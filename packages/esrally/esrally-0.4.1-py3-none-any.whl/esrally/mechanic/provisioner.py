import os
import glob
import shutil
import logging

from esrally import config
from esrally.utils import io, versions

logger = logging.getLogger("rally.provisioner")


class Provisioner:
    """
    The provisioner prepares the runtime environment for running the benchmark. It prepares all configuration files and copies the binary
    of the benchmark candidate to the appropriate place.
    """

    def __init__(self, cfg):
        self._config = cfg
        self.preserve = self._config.opts("provisioning", "install.preserve")

    # TODO #71: This should be split into an environment independent configuration (car) and environment dependent configuration (http_port)
    def prepare(self, car, http_port):
        self._install_binary()
        self._configure(car, http_port)

    def cleanup(self):
        install_dir = self._install_dir()
        if self.preserve:
            logger.info("Preserving benchmark candidate installation at [%s]." % install_dir)
            print("\nRally will keep the benchmark candidate including all data at [%s].\nRemember to delete it when you don't need it "
                  "anymore as it will take up a significant amount of disk space." % install_dir)
        else:
            logger.info("Wiping benchmark candidate installation at [%s]." % install_dir)
            if os.path.exists(install_dir):
                shutil.rmtree(install_dir)
            data_paths = self._config.opts("provisioning", "datapaths", mandatory=False)
            if data_paths is not None:
                for path in data_paths:
                    if os.path.exists(path):
                        shutil.rmtree(path)

    def _install_binary(self):
        binary = self._config.opts("builder", "candidate.bin.path")
        install_dir = self._install_dir()
        logger.info("Preparing candidate locally in %s." % install_dir)
        io.ensure_dir(install_dir)
        if not self.preserve:
            print("Rally will wipe the benchmark candidate directory [%s] after the benchmark.\n" % install_dir)

        logger.info("Unzipping %s to %s" % (binary, install_dir))
        io.decompress(binary, install_dir)
        binary_path = glob.glob("%s/elasticsearch*" % install_dir)[0]
        self._config.add(config.Scope.benchmark, "provisioning", "local.binary.path", binary_path)

    def _configure(self, car, http_port):
        self._configure_logging(car)
        self._configure_cluster(car, http_port)

    def _configure_logging(self, car):
        log_cfg = car.custom_logging_config
        if log_cfg:
            logger.info("Replacing pre-bundled ES log configuration with custom config: [%s]" % log_cfg)
            binary_path = self._config.opts("provisioning", "local.binary.path")
            open("%s/config/logging.yml" % binary_path, "w").write(log_cfg)

    def _configure_cluster(self, car, http_port):
        binary_path = self._config.opts("provisioning", "local.binary.path")
        logger.info("Using port [%d]" % http_port)
        env_name = self._config.opts("system", "env.name")
        additional_config = car.custom_config_snippet
        data_paths = self._data_paths(car)
        logger.info("Using data paths [%s]" % data_paths)
        self._config.add(config.Scope.challenge, "provisioning", "local.data.paths", data_paths)
        s = open("%s/config/elasticsearch.yml" % binary_path, "r").read()
        s += "\ncluster.name: %s\n" % "benchmark.%s" % env_name
        s += self.number_of_nodes(car)
        s += "\npath.data: %s" % ", ".join(data_paths)
        s += "\nhttp.port: %d-%d" % (http_port, http_port + 100)
        s += "\ntransport.tcp.port: %d-%d" % (http_port + 100, http_port + 200)
        if additional_config:
            s += "\n%s" % additional_config
        open("%s/config/elasticsearch.yml" % binary_path, "w").write(s)

    def number_of_nodes(self, car):
        distribution_version = self._config.opts("source", "distribution.version", mandatory=False)
        configure = False
        if versions.is_version_identifier(distribution_version):
            major_version = int(versions.components(distribution_version)["major"])
            if major_version >= 2:
                configure = True
        else:
            # we're very likely benchmarking from sources which is ES 5+
            configure = True
        return "\nnode.max_local_storage_nodes: %d" % car.nodes if configure else ""

    def _data_paths(self, car):
        binary_path = self._config.opts("provisioning", "local.binary.path")
        data_paths = self._config.opts("provisioning", "datapaths")
        if data_paths is None:
            return ["%s/data" % binary_path]
        else:
            # we have to add the car name here as we need to preserve data potentially across runs
            return ["%s/%s" % (path, car.name) for path in data_paths]

    def _install_dir(self):
        root = self._config.opts("system", "challenge.root.dir")
        install = self._config.opts("provisioning", "local.install.dir")
        return "%s/%s" % (root, install)

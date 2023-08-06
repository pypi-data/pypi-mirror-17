quark *;
include io/datawire/quark/runtime/RuntimeSpi.java;

namespace quark {
namespace spi {

    interface RuntimeSpi extends Runtime {
        macro RuntimeSpi() $java{io.datawire.quark.runtime.RuntimeSpi.Factory.create()}
        $py{_RuntimeFactory.create()}
        $rb{::DatawireQuarkCore::Runtime.new}
        $js{_qrt.RuntimeFactory.create()};
    }


    class RuntimeFactory {
        static RuntimeFactory factory = new RuntimeFactory();

        static bool enable_tracing = true;
        static bool env_checked = false;

        quark.Runtime makeRuntime() {
            RuntimeSpi spi = new RuntimeSpi();
            Runtime api;
            if (!env_checked) {
                enable_tracing = (logging.Config._getOverrideIfExists() != null);
                env_checked = true;
            }
            if (enable_tracing) {
                api = new quark.spi_api_tracing.RuntimeProxy(spi);
            } else {
                api = new quark.spi_api.RuntimeProxy(spi);
            }
            return api;
        }
    }
}}

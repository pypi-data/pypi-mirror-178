import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


ViewsParts.DeviceViewForRedesign {
    Settings.DataImport {}
    Settings.MalfunctionBattery {}
    Settings.SignalStrength {}
    Settings.Connection {}
    Settings.RoutedThroughReX {}
    Settings.BatteryCharge {
        isBad: device && device.is_battery_broken || device.battery <= 20 && !device.battery_charging
        atomTitle.subtitle: {
            if (device && device.is_battery_broken) {
                return tr.error
            }
            if (device.battery_charging) {
                return tr.charging
            }
            if (device.battery == "N/A") {
                return tr.na
            }
            return device.battery + " %"
        }
    }
    Settings.Tamper {}
    Settings.ExternalPower {}
    Settings.TemporaryDeactivation {}
}

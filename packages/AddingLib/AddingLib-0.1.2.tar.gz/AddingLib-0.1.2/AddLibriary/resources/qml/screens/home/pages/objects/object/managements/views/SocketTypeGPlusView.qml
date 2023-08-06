import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


ViewsParts.DeviceViewForRedesign {
    Settings.DataImport {}
    Settings.SignalStrength {}
    Settings.Connection {}
    Settings.RoutedThroughReX {}
    Settings.Active {
        atomTitle.subtitle: {
            if (device.turned_on === "N/A") return tr.na
            return (device.turned_on === "CHANNEL_1_ON") ? tr.yes : tr.no
        }
    }
   Settings.Current {
        isBad: {
            if (device.current == "N/A") return false
            if (device.current > 11) return true
            return false
        }
    }
   Settings.Voltage {
        isBad: {
            if (device.voltage == "N/A") return false
            return device.voltage < 185 || device.voltage > 252
        }
   }
    Settings.CurrentProtectionThreshold {}
    Settings.VoltageProtection {
        atomTitle.subtitle: !device.voltage_protection_off ? tr.on : tr.off
    }
    Settings.ArcFaultDetect {}
    Settings.Power {}
    Settings.ElectricEnergyConsumed {}
    Settings.LastConsumptionReset {}
    Settings.TemporaryDeactivation {}
}
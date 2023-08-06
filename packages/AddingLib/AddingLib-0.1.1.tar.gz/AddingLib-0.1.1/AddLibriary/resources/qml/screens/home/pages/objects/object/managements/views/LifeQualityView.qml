import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


ViewsParts.DeviceView2 {
    DS3.SettingsContainer {
        Settings.AirQualitySensorsMalfunctions {}
        Settings.DataImport2 {}
        Settings.TemperatureLifeQuality {}
        Settings.Humidity {}
        Settings.CO2 {}
    }
    DS3.Spacing {
        height: 24
    }
    DS3.SettingsContainer {
        Settings.SignalStrength {}
        Settings.Connection2 {}
        Settings.BatteryChargeBoolean {}
        Settings.AccelerationAware {}
        Settings.RoutedThroughReX2 {}
        Settings.TemporaryDeactivation2 {}
    }
}
import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as ViewRows
import "qrc:/resources/qml/components/911/DS3" as DS3


LightSwitchView {
    connection: DS3.SettingsContainer {
        id: connectionContainer

        width: parent.width

        ViewRows.TwoWaySwitchType {}
        ViewRows.SignalStrength {}
        ViewRows.Connection {}
        ViewRows.RoutedThroughReX {}
    }
}
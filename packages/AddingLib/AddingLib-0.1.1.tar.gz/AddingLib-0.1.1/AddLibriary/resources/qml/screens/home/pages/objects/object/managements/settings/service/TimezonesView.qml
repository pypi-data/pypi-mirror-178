import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: timezonesView

    width: parent.width
    height: timezonesListView.height

    ListView {
        id: timezonesListView

        width: parent.width
        height: contentHeight

        clip: true
        boundsBehavior: Flickable.StopAtBounds
        spacing: 4

        model: timezones.filtered

        delegate: DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSingleSelection {
                width: timezonesListView.width

                atomTitle.title: readable
                switchChecked: () => {
                    if (!timezonesItem.service) {
                        selected = zone.id
                        return
                    }
                    timeZones.subtitle = readable
                    timeZones.selectedId = zone.id
                    timezoneLoader.setSource("")
                }
                checked: selected == zone.id
            }
        }
    }
}


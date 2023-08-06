import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/images.js" as Images


DS3.Popup {
    id: popup

//  If current folder is "Devices"
    property bool devicesChosen: false

    width: 500
    height: 704

    sideMargins: 24

    header: Item {
        height: navBar.height + folderControl.height

        DS3.NavBarModal {
            id: navBar

            anchors.top: parent.top

            onClosed: () => {
                popup.close()
            }
        }

        DS3.FolderControl {
            id: folderControl

            anchors.bottom: parent.bottom

            model: [
                { text: tr.buttons_import, index: 0 },
                { text: tr.devices_in_migration, index: 1 }
            ]

            onCurrentIndexDiffer: {
                folderControl.currentIndex = index
                devicesChosen = currentIndex
            }
        }
    }

    DS3.Spacing {
        height: 48
    }

    DS3.InfoContainer {
        anchors.horizontalCenter: parent.horizontalCenter

        titleComponent.text: {
            if (devicesChosen) {
                return repeater.count ? tr.devices_go_automatically_title : tr.all_devices_transfered_new
            } else {
                return repeater.count ? tr.press_button_import_title : tr.all_controls_transfered_new
            }
        }
        descComponent.text: devicesChosen ? tr.devices_go_automatically_descr :  tr.press_button_import_descr
        descComponent.visible: repeater.count
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Icon {
        anchors.horizontalCenter: parent.horizontalCenter

        source: "qrc:/resources/images/Athena/migration/Ok-L.svg"
        visible: !repeater.count
    }

    Column {
        width: parent.width

        spacing: 1

        Repeater {
            id: repeater

            width: parent.width

            model: devicesChosen ? filteredWithoutButtonsDevicesInProgress : filteredButtonsDevicesInProgress
            visible: devicesChosen ? filteredWithoutButtonsDevicesInProgress.length : filteredButtonsDevicesInProgress.length

            DS3.SettingsContainerItem {
                id: deviceDelegate

                Connections {
                    target: devicesListView.list

                    onCountChanged: {
                        deviceDelegate.isFirst = index == 0
                        deviceDelegate.isLast = index == repeater.model.length - 1
                    }
                }

                width: parent.width
                height: childrenRect.height

                isFirst: index == 0
                isLast: index == repeater.model.length - 1

                DS3.InfoStatus {
                    width: parent.width

                    color: ui.ds3.figure.transparent
                    source: {
                        if (device.obj_type == '1d') {
                            return Images.get_image(device.obj_type, "Medium", device.input_type, device.custom_alarm_available_v2 ? device.custom_alarm_S2 : device.custom_alarm)
                        }
                        return Images.get_image(device.obj_type, "Medium", device.color, "0", device.subtype)
                    }
                    atomTitle {
                        title: device.name || ""
                        subtitle: tr.in_progress_now
                        subtitleColor: ui.ds3.figure.positiveContrast
                    }
                }
            }
        }
    }
}
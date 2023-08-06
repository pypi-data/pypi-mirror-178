import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/js/utils.js" as Utils


DS3Popups.PopupStep {
    property var rangeExtender: null
    property var isReX2: false
    property var devices_model: {
        if (isReX2) {
            management.filtered_devices_for_rex2.updateModel()
            return management.filtered_devices_for_rex2
        }
        else {
            management.filtered_devices_for_rex.updateModel()
            return management.filtered_devices_for_rex
        }
    }
    property var allDevices: Array.from(Array(devices_model.length).keys()).map(idx => devices_model.get(idx))
    property var selectedDevices: null
    property var initialSelectedDevices: null

    Component.onCompleted: {
        selectedDevices = allDevices.reduce((object, device) => {
            object[device.id] = device.assigned_extender == rangeExtender.device_index
            return object
        }, {})
        initialSelectedDevices = JSON.parse(JSON.stringify(selectedDevices))
    }

    height: maxStepHeight

    Connections {
        target: app

        onAltActionSuccess: {
            goBack()
        }
    }

    title: tr.select_devices

    DS3.ListView {
        id: devicesListView

        width: parent.width
        height: maxStepHeight

        visible: !noRexDevices.visible

        list {
            model: devices_model
            delegate: DS3.DeviceSelectionMulti {
                id: deviceDelegate

                width: parent.width

                property int indexRef: index
                property var old_state: device.assigned_extender == rangeExtender.device_index
                property var roomName: room_name

                objectName: "delegate"
                atomTitle.title: device.name
                imageSource: Images.get_image(device.obj_type, "Small", device.color, "0", device.subtype)
                checked: !!selectedDevices[device.id]
                isLast: deviceDelegate.ListView.nextSection != deviceDelegate.ListView.section

                clickedArea.onClicked: {
                    selectedDevices[device.id] = !selectedDevices[device.id]
                    selectedDevicesChanged()
                }
            }
            header: Item {}
            spacing: 1
            section.property: "room_name"
            section.delegate: Item {
                property var sectionRef: section
                property alias sectionText: sectionLabel.text
                property bool allDevicesSelected: Object.keys(selectedDevices).every(
                    (_, idx) => {
                        const device = devices_model.get(idx)
                        return device.room_name != section || !!selectedDevices[device.id]
                    }
                )

                width: deviceDelegate.width
                height: 52

                objectName: "section"
                Rectangle {
                    width: devicesListView.width - 48
                    height: 16

                    anchors {
                        top: parent.top
                        topMargin: 24
                        left: parent.left
                    }

                    radius: height / 2
                    color: ui.ds3.bg.high
                }

                Rectangle {
                    id: sectionBackground

                    width: devicesListView.width - 48
                    height: 19

                    anchors {
                        bottom: parent.bottom
                        bottomMargin: 1
                        left: parent.left
                    }

                    color: ui.ds3.bg.high
                }

                DS3.Text {
                    width: 310

                    anchors {
                        left: sectionBackground.left
                        leftMargin: 16
                        bottom: sectionBackground.bottom
                        bottomMargin: 4
                    }

                    text: section
                }

                DS3.Text {
                    id: sectionLabel

                    width: undefined

                    anchors {
                        right: sectionBackground.right
                        rightMargin: 16
                        bottom: sectionBackground.bottom
                        bottomMargin: 4
                    }

                    verticalAlignment: Text.AlignVCenter
                    color: ui.ds3.figure.interactive
                    text: allDevicesSelected ? tr.uncheck_all : tr.check_all
                    style: ui.ds3.text.body.SRegular

                    MouseArea {
                        anchors.fill: parent

                        onClicked: {
                            allDevices.forEach(device => {
                                if (device.room_name == section) selectedDevices[device.id] = !allDevicesSelected
                            })
                            selectedDevicesChanged()
                        }
                    }
                }
            }
        }
    }

    Column {
        id: noRexDevices

        width: parent.width

        visible: !devices_model.length || devices_model.length == 0

        DS3.Spacing {
            height: 24
        }

        DS3.InfoContainer {
            width: parent.width - 80

            anchors.horizontalCenter: parent.horizontalCenter

            imageType: DS3.InfoContainer.ImageType.PlugImage
            imageSource: "qrc:/resources/images/Athena/common_icons/HubEmpty.svg"
            descComponent.text: tr.no_rex_devices_yet
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width - 48

            anchors.horizontalCenter: parent.horizontalCenter

            visible: !isReX2

            DS3.InfoTitleButtonIcon {
                atomTitle.title: tr.rex_devices_help
                buttonIcon.source: "qrc:resources/images/Athena/common_icons/ExternalLink-M.svg"

                onRightControlClicked: {
                    var locales = ["en", "ru", "uk", "es", "de", "it", "fr"]
                    var locale = app.get_locale()
                    if (locale == "ua") {
                        locale = "uk"
                    }
                    if (!locales.includes(locale)) {
                        locale = "en"
                    }

                    var link = "https://support.ajax.systems/" + locale + "/faqs/rex-compatible-devices/"
                    Qt.openUrlExternally(link)
                }
            }
        }
    }


    footer: DS3.ButtonBar {
        id: saveButton

        visible: devicesListView.count != 0 && devicesListView.visible
        enabled: JSON.stringify(initialSelectedDevices) != JSON.stringify(selectedDevices)
        hasBackground: true
        button {
            text: tr.save
            onClicked: {
                var devices = []
                allDevices.forEach(device => {
                    var old = initialSelectedDevices[device.id]
                    var choice = selectedDevices[device.id]

                    if (old == false && choice == true && !(!!hub && hub.online && !!device && device.online)) {
                        Popups.popupByPath(
                            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                            {
                                isVertical: true,
                                title: util.insert(tr.rex_is_offline, [device.name]),
                                text: tr.rex_is_offline_descr,
                                firstButtonText: tr.i_will_check,
                                secondButtonText: tr.rollback_changes,
                                isSecondButtonRed: true,
                                secondButtonCallback: () => {
                                    goBack()
                                }
                            }
                        )
                        return
                    }

                    if (old != choice) {
                        let device_info = {}

                        device_info["type"] = device.obj_type
                        device_info["id"] = device.id
                        device_info["assigned_extender"] = choice ? rangeExtender.device_index: 0

                        devices.push(device_info)
                    }
                })
                app.hub_management_module.update_objects_settings(devices, {"emit_alt_signal": true})
            }
        }
    }
}
import QtQuick 2.12

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.ScrollView {
    default property alias data: container.data
    property var device: null
    readonly property bool isYavirDevice: ["26", "27", "28", "29"].includes(device.obj_type)

    Connections {
        target: device

        onOpenEthConnectionDetails: {
            Popups.popupByPath(
                "qrc:/resources/qml/screens/home/pages/objects/object/popups/EthConnectionDetails.qml", {
                    "device": device
                }
            )
        }
    }

    opacity: hub && hub.online && device.online ? 1.0 : 0.3
    padding: 24

    ViewsParts.DeviceNameRoom {}
    DS3.DeviceHeaderInfo {
        imagePath: {
            if (device.obj_type == "2e") return Images.get_image(device.card_type, "Large", device.color)
            if (device.obj_type == "26") {
                return Images.get_image(device.input_is_tamper == 1 ? "26-wired-tamper" : "26-wired-intrusion", "Large")
            }
            if (device.obj_type == "28") {
                return Images.get_image(device.device_type != 2 ? "28-keypad-yavir" : "28-reader-yavir", "Medium")
            }
            if (device.obj_type == "1d") {
                return Images.get_image(device.obj_type, "Large", device.input_type, device.custom_alarm_available_v2 ? device.custom_alarm_S2 : device.custom_alarm)
            }
            return Images.get_image(device.obj_type, "Large", device.color, "0", device.subtype)
        }
    }
    DS3.SettingsContainer {
        id: container

        width: parent.width
        // boileplate for moving from Settings.*.qml to model generated in python
        Repeater {
            id: repeater

            model: device.view_rows_list

            Column {
                width: parent.width

                DS3.Spacing {
                    height: 24
                }

                Repeater {
                    model: modelData['title']

                    Column {
                        width: parent.width

                        DS3.TitleSection {
                            text: modelData['titleText']
                            forceTextToLeft: true
                            isBgTransparent: true
                            isCaps: true
                        }
                    }
                }

                DS3.SettingsContainer {
                    Repeater {
                        model: modelData['rows']

                        Column {
                            width: parent.width

                            DS3.InfoSignal {
                                id: infoSignal

                                visible: modelData["isInfoSignal"] === true

                                atomTitle.title: modelData["title"]
                                leftIcon.source: modelData["icon"]
                                atomConnection.strength: visible ? modelData["value"] || 0 : 0
                            }

                            DS3.InfoStatus {
                                id: infoStatus

                                width: parent.width

                                visible: modelData["isInfoImage"] === true
                                atomTitle.title: modelData["title"]
                                source: modelData["icon"]
                            }

                            DS3.InfoTitle {
                                id: info_row

                                visible: !infoSignal.visible && !infoTitleButtonIcon.visible && !infoStatus.visible
                                atomTitle {
                                    title: modelData["title"]
                                    subtitle: modelData["value"] || ""
                                }
                                leftIcon.source: modelData["icon"]
                                status: ui.ds3.status[modelData["status"]]
                            }


                            DS3.InfoTitleButtonIcon {
                                id: infoTitleButtonIcon

                                visible: modelData["isInfoTitleButtonIcon"] === true
                                atomTitle {
                                    title: modelData["title"]
                                    subtitle: modelData["value"] || ""
                                    titleColor: !!modelData["value"] ? ui.ds3.figure.base : statusColor || ui.ds3.figure.base
                                }
                                leftIcon.source: modelData["icon"]
                                status: ui.ds3.status[modelData["status"]]
                                buttonIcon.source: modelData["buttonIcon"] || ""
                                buttonIcon.color: ui.ds3.figure.interactive

                                onRightControlClicked: {
                                    if (modelData["callbackSignalName"]) {
                                        device[modelData["callbackSignalName"]]()
                                    }
                                    if (modelData["raiseErrPopupOnClicked"]) {
                                        Popups.error_popup(modelData["raiseErrPopupOnClicked"])
                                    }
                                    if (modelData["raiseModalInfoPopupOnClicked"]) {
                                        Popups.popupByPath(
                                            "qrc:/resources/qml/components/911/DS3/popups/ModalInfo.qml",
                                            {sections: modelData["raiseModalInfoPopupOnClicked"]}
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    DS3.Spacing {
        height: 24
    }
    Loader {
        id: footerLoader

        width: parent.width
        height: childrenRect.height

        source: {
            if (device.obj_type == "1d") return "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts/MTDeviceFooter.qml"
            return isYavirDevice ? "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts/YavirDeviceFooter.qml"
            : "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts/DeviceFooter.qml"
        }
    }
}
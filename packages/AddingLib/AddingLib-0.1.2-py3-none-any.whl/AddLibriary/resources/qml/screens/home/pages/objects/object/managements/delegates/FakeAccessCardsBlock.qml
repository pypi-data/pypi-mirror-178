import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/"
import "qrc:/resources/qml/components/desktop"
import "qrc:/resources/js/popups.js" as Popups

Item {
    id: delegate

    property var hidden: true

    property var trueIndex: index
    property var currentTab: {
        if (appUser.company_id) return equipment.currentTab
        return hubSidebar.currentTab
    }
    property alias mtrDevices: mtrDevices

    height: {
        if (mtrDevices.model) return currentTab == "DEVICES" ? mtrDevices.height + 72 + (!hidden && mtrDevices.model.length > 0) : 72
    }

    opacity: (!hub || !hub.online) ? 0.6 : 1

    Row {
        height: 72
        width: parent.width

        anchors.top: parent.top

//        key::access_device
        Item {
            width: 8
            height: parent.height
        }

        Image {
            width: 72
            height: 72

            source: "qrc:/resources/images/desktop/delegates/PassTag/PassTagMedium.png"
            fillMode: Image.PreserveAspectFit
        }

        Item {
            width: 16
            height: parent.height
        }

        Custom.FontText {
            width: contentWidth
            height: contentHeight

            anchors.verticalCenter: parent.verticalCenter

            text: tr.access_device
            color: ui.colors.white
            font.pixelSize: 16
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
        }
    }

    Item {
        id: triangleItem

        width: 32
        height: 64

        anchors {
            right: parent.right
            rightMargin: 16
            top: parent.top
        }

        Custom.Triangle {
            anchors.centerIn: parent
            rotation: delegate.hidden ? 0 : 180
            colorTriangle: ui.colors.green1
        }
    }

    Custom.HandMouseArea {
        propagateComposedEvents: true

        onClicked: {
            delegate.hidden = !delegate.hidden
//            mouse.accepted = false
        }
    }

    ListView {
        id: mtrDevices

        width: parent.width
        height: parent.hidden ? 0 : contentHeight

        anchors.bottom: parent.bottom

        clip: true
        currentIndex: -1
        interactive: false
        model: if (device) return device.cards

        onCurrentIndexChanged: {
            if (mtrDevices.model) {
                devicesItem.device = mtrDevices.model.get(mtrDevices.currentIndex)
                if (devicesItem.device == null) return
                deviceLoader.setSource(devicesItem.device.device_view, {"device": devicesItem.device})
            }
        }

        header: Item {
            width: parent.width
            height: 50

            Rectangle {
                width: parent.width
                height: 48

                anchors.verticalCenter: parent.verticalCenter

                color: ui.colors.dark3

                Custom.SearchField {
                    id: searchField

                    width: parent.width - 8
                    height: 38

                    anchors.centerIn: parent

                    placeHolderText: tr.search_devices

                    onSearchStarted: {
                        mtrDevices.model.set_filter(data)
                        mtrDevices.currentIndex = -1
                    }

                    Connections {
                        target: delegate
                        onHiddenChanged: {
                            searchField.control.text = ""
                            mtrDevices.model.set_filter("")
                        }
                    }
                }
            }
        }


        delegate: Rectangle {
            id: deviceDelegateMt

            property var settingsVisible: !devices.withoutSettingIcon

            width: parent.width
            height: 72 + (mtrDevices.model.length - 1 != index)

            color: ui.colors.black

            Custom.RoundedRect {
                width: parent.width
                height: 72

                radius: 10
                color: mtrDevices.currentIndex == index ? ui.colors.black : ui.colors.dark3

                topRightCorner: false  // (index == 0 && devices.list.currentIndex == delegate.trueIndex) || (index > 0 && index - 1 == mtrDevices.currentIndex)
                bottomRightCorner: false  // (index < mtrDevices.model.length - 1 && index + 1 == mtrDevices.currentIndex)

                Custom.HandMouseArea {
                    onClicked: {
                        devices.list.currentIndex = -1
                        mtrDevices.currentIndex = index
                    }
                }
            }

            IconSettings { visible: settingsVisible }

            Loader {
                id: loader

                width: parent.width
                height: 72

                anchors.top: parent.top

                source: device ? device.delegate : ""
            }
        }

        footer: Footer {
            id: mtrFooter

            height: visible ? 72 : 0

            roundRect.color: ui.colors.dark3

            btn {
                color: "white"
                text: tr.add_access_device

                backgroundItem {
                    color: ui.colors.dark4
                    border.width: 0
                }
            }

            Rectangle {
                id: spacer

                width: parent.width
                height: mtrFooter.visible ? 1 : 0

                color: ui.colors.black
            }

            topRightCorner: false  // mtrDevices.currentIndex == mtrDevices.model.length - 1 && mtrDevices.model.length > 0
            bottomRightCorner: {
                return false

                var prevDev = devices.list.model.get(devices.list.currentIndex - 1)
                return prevDev && prevDev.class_name == "multi_transmitter"
            }

            visible: {
                if (!device) return false
                if (!device.count_keypads_with_nfc) return false
                if (!hub.online) return false
                if (hub.two_stage_arming_status) return false
                if (hub.state == "ARMED" || hub.state == "NIGHT_MODE") return false
                if (hub.two_stage_arming_progress_status > 1) return false
                if (!hub.current_user.device_edit_access) return false
                return true
            }

            btn.onClicked: {
                if (!device.is_kpp_kpc_here) {
                    if (!device.is_kpp_here() && device.kpp_count && !device.kpc_count) {
                        Popups.text_popup(tr.turn_on_nfc_info, tr.turn_on_nfc_in_kpp)
                    } else if (!device.is_kpc_here() && device.kpc_count && !device.kpp_count) {
                        Popups.text_popup(tr.turn_on_nfc_info, tr.turn_on_nfc_in_kpc)
                    } else {
                        Popups.text_popup(tr.turn_on_nfc_info, tr.turn_on_nfc_in_kpp_kpc)
                    }
                } else {
                    addAccessCardPopup("")
                }
            }
        }

        Connections {
            target: devices

            onResetMtrDevicesIndex: {
                mtrDevices.currentIndex = -1
            }
        }
    }
}

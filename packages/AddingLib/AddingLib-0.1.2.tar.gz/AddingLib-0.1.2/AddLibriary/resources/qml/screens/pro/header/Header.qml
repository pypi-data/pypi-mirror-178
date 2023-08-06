import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    height: 64
    width: parent.width

    color: ui.colors.black

    property var popup: null
    property var currentState: 0
    property var sidebarVisible: false
    property alias sidebarOpenArea: sidebarOpenArea

    onSidebarVisibleChanged: {
        parent.forceActiveFocus()
    }

    Connections {
        target: popup

        onClosed: hubsStack.forceActiveFocus()
    }

    RowLayout {
        anchors.fill: parent
        spacing: 1
        Item {
            Layout.minimumWidth: 64
            width: 64
            height: 64

            Custom.WindowsFuck {}

            Image {
                sourceSize.width: 64
                sourceSize.height: 64
                source: "qrc:/resources/images/icons/a-logo-pro.svg"
                anchors.centerIn: parent
            }
        }

        Item {
            Layout.minimumWidth: 270
            width: 64
            height: 64

            Rectangle {
                width: 1
                height: parent.height
                color: ui.colors.middle1
                opacity: 0.2

                anchors {
                    right: parent.right
                }
            }

            Custom.FontText {
                property var available: [tr.hubs, tr.a911_company]
                color: ui.colors.white
                text: available[currentState]
                font.pixelSize: 24
                font.weight: Font.Thin
                visible: !sidebarVisible
                anchors {
                    verticalCenter: parent.verticalCenter
                    left: parent.left
                    leftMargin: 12
                }
            }

            Custom.Triangle {
                visible: !sidebarVisible
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                    rightMargin: 24
                }
            }

            Custom.HandMouseArea {
                id: sidebarOpenArea
                anchors.fill: parent
            }
        }

        Item {
            id: addHubItem

            Layout.fillHeight: true
            Layout.minimumWidth: 196
            Layout.maximumWidth: 196
            Layout.leftMargin: 16

            Custom.Button {
                id: addHubButton

                visible: currentState == 0 && hubsStack.managementLoader.source == ""
                width: parent.width
                text: tr.add_hub
                transparent: true
                color: ui.colors.green1
                anchors.centerIn: parent

                onClicked: {
                    application.debug("pro -> header -> add hub popup")
                    parent.forceActiveFocus()

                    DesktopPopups.popupByPath("qrc:/resources/qml/screens/pro/header/AddHubPopup.qml")
                }

                /* ---------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "pro_hubs_add-hub_button"
                Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                Accessible.role: Accessible.Button
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    addHubButton.clicked(true)
                }
                /* ---------------------------------------------------- */
            }
        }

        Item {
            id: refreshButtonItem

            Layout.fillHeight: true
            Layout.minimumWidth: 112
            Layout.maximumWidth: 112
            Layout.leftMargin: 32
            Custom.RefreshButton {
                id: refreshButton

                visible: currentState == 0 && hubsStack.managementLoader.source == ""

                refreshArea.onClicked: {
                    home.reloadAllHubs()
                }
            }

            Connections {
                target: home

                onReloadAllHubs: {
                    refreshButton.refreshAnim.start()
                }
            }
        }


        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        Custom.TimeSync {}

        Item {
            id: searchItem

            Layout.fillHeight: true
            Layout.minimumWidth: 220
            Layout.maximumWidth: 220
            Layout.rightMargin: 16

            Custom.SearchField {

                width: parent.width
                height: 42

                visible: currentState == 0 && hubsStack.managementLoader.source == ""
                anchors.centerIn: parent
                placeHolderText: tr.a911_search
                color: ui.colors.dark3
                radius: control.activeFocus ? 0 : height / 2
                control.leftPadding: 16

                onSearchStarted: {
                    hubsStack.updateFilter(data)
                    // TODO: remove old pro hubs model
                    // appCompany.pro_hubs_model.searched.set_filter(data)
                }
            }
        }


        Rectangle {
            Layout.minimumWidth: 76
            Layout.maximumWidth: 76
            Layout.fillHeight: true
            Layout.rightMargin: 12
            color: "transparent"

            Rectangle {
                width: 1
                height: parent.height
                color: ui.colors.white
                opacity: 0.1
            }

            Custom.UserImage {
                id: currentUserOrCompanyImage

                property var isUserImage: {
                    if (!appUser) return false
                    if (!appUser.data) return false
                    if (!appUser.data.user_info) return false
                    if (!appUser.data.user_info.image_urls) return false
                    if (!appUser.data.user_info.image_urls.base_path) return false

                    return true
                }
                width: 42
                height: 42

                userName: {
                    if (!appUser || !appUser.data || !appUser.data.user_info) return ""

                    var name = ""
                    if (appUser.data.user_info.first_name) {
                        name += appUser.data.user_info.first_name + " "
                    }
                    if (appUser.data.user_info.last_name) {
                        name += appUser.data.user_info.last_name
                    }
                    return name
                }

                imageSource: isUserImage ? appUser.data.user_info.image_urls.base_path + appUser.data.user_info.image_urls.small : ""
                anchors {
                    left: parent.left
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "pro_account_image"
                Accessible.description: isUserImage ? imageSource : "text:" + userName
                Accessible.role: Accessible.Graphic
                /* ------------------------------------------------ */
            }

            Custom.Triangle {
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                }
            }

            Custom.HandMouseArea {
                id: proAccountArea

                onClicked: {
                    if (popup) {
                        popup.close()
                        popup = null
                    } else {
                        application.debug("pro -> header -> user popup")
                        parent.forceActiveFocus()
                        popup = Popups.user_popup()
                    }
                }

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "pro_account_area"
                Accessible.description: "<button enabled=" + Accessible.checkable + ">" + "account:pro" + "</button>"
                Accessible.role: Accessible.Button
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    proAccountArea.clicked(true)
                }
                /* ------------------------------------------------ */
            }
        }

        Rectangle {
            Layout.minimumWidth: 64
            Layout.maximumWidth: 64
            Layout.fillHeight: true
            color: "transparent"

            Rectangle {
                width: 1
                height: parent.height
                color: ui.colors.white
                opacity: 0.1
            }

            Custom.ConnectionStatus {}
        }
    }
}

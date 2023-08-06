import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    height: 64
    width: parent.width
    color: ui.colors.black

    property var currentState: {
        if (home.loginTab) {
            if (home.loginTab == "monitoring" && companyAccess.MONITORING) return 0
            if (home.loginTab == "journal" && companyAccess.JOURNAL) return 1
            if (home.loginTab == "objects" && companyAccess.OBJECTS) return 2
            if (home.loginTab == "company" && companyAccess.COMPANY) return 3
        }

        var idx = 0

        if (!companyAccess.MONITORING) idx++
        else return idx

        if (!companyAccess.JOURNAL) idx++
        else return idx

        if (!companyAccess.OBJECTS) idx++
        else return idx

        if (!companyAccess.COMPANY) idx++
        else return idx

        return idx
    }
    property var sidebarVisible: false
    property alias sidebarOpenArea: sidebarOpenArea
    property var popup: null
    property alias testArea: testArea

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
            Layout.minimumWidth: 269
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
                property var available: [tr.a911_monitoring, tr.a911_list, tr.a911_objects, tr.a911_company]
                color: ui.colors.white
                text: {
                    if (currentState == 4) return ""
                    return available[currentState]
                }
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
            Layout.minimumWidth: 64
            Layout.fillWidth: true
            height: 64

            ToggleBar {
                visible: {
                    if (!companyAccess.MONITORING) return false
                    return currentState != 3 && currentState != 4
                }
                events: appCompany.incidents_model.new_and_viewing_count
                in_progress: appCompany.incidents_model.processing_count
                sleep: appCompany.incidents_model.slept_count
            }
        }

        Item {
            id: possibleSearch
            Layout.minimumWidth: 64
            Layout.fillHeight: true

            Item {
                width: 72
                height: parent.height
                visible: currentState == 2
                anchors.right: parent.right

                Rectangle {
                    width: 40
                    height: width
                    radius: height
                    color: ui.colors.dark4
                    anchors.centerIn: parent

                    Image {
                        sourceSize.width : 40
                        sourceSize.height : 40
                        source: "qrc:/resources/images/icons/a-search-icon.svg"
                        anchors.centerIn: parent
                    }

                    Custom.HandMouseArea {
                        onClicked: {
                            application.debug("company -> header -> search facilities")
                            Popups.facilities_search_popup(objectsStack)
                        }
                    }
                }
            }
        }

        Custom.TimeSync {}

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
                width: 42
                height: 42

                userName: {
                    if (!appCompany || !appCompany.data || !appCompany.data.short_name) return ""
                    return appCompany.data.short_name
                }

                imageSource: {
                    if (!appCompany || !appCompany.data || !appCompany.data.company_logo || !appCompany.data.company_logo.image_id || !appCompany.data.company_logo.images) return ""
                    return util.get_image_with_resolution(appCompany.data.company_logo.images, "128x128")
                }

                anchors {
                    left: parent.left
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "company_account_image"
                Accessible.description: imageSource ? imageSource : "text:" + userName
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
                id: testArea

                onClicked: {
                    if (popup) {
                        popup.close()
                        popup = null
                    } else {
                        application.debug("company -> header -> user popup")
                        popup = Popups.user_popup()
                    }
                }

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "company_account_area"
                Accessible.description: "<button enabled=" + Accessible.checkable + ">" + "account:company_" + appUser.company_id + "</button>"
                Accessible.role: Accessible.Button
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    testArea.clicked(true)
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

            Custom.HandMouseArea {
                visible: false
                pressAndHoldInterval: 5000

                onPressAndHold: {
                    // app.company_module.delete_company()
                }
            }
        }
    }
}

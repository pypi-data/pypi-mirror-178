import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/screens/pro/header/"
import "qrc:/resources/qml/screens/pro/sidebar/"
import "qrc:/resources/qml/screens/pro/pages/hubs/"
import "qrc:/resources/qml/screens/pro/pages/company/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: home
    anchors {
        top: parent.top
        left: parent.left
        right: parent.right
        bottom: parent.bottom
        bottomMargin: {
            if (notActualVersionNotification.visible) return notActualVersionNotification.height
            return 0
        }
    }

    signal destroyHub()
    signal reloadAllHubs()

    property var openOnNotificationsTab: ""

    onDestroyHub: {
        application.debug("pro -> hubs -> hub -> destroy")

        application.closeHubSettings()

        hubsStack.managementLoader.source = ""
        appCompany.pro_hubs_model.unsubscribe()
        app.hubsView.chooseHub("", "")
        home.reloadAllHubs()
    }

    onReloadAllHubs: {
        hubsStack.reloadHubIndices()
    }

    OfflinePopup {
        id: offlinePopup
        destructOnClose: false

        Connections {
            target: app

            onOnlineChanged: {
                /*
                if (app.online) {
                    application.debug("OFFLINE POPUP -> CLOSE")
                    offlinePopup.close()
                } else {
                    application.debug("OFFLINE POPUP -> OPEN")
                    offlinePopup.open()
                }
                */
            }
        }
    }

    DS3.NavBarMain { id: navBarMain }

    Header {
        id: header

        height: __figma_46_headers_features__ ? 0 : 64

        anchors.top: navBarMain.bottom

        visible: !navBarMain.visible
        sidebarOpenArea.onClicked: {
            header.sidebarVisible = !header.sidebarVisible
        }
    }

    StackLayout {
        anchors {
            top: header.bottom
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }

        currentIndex: header.currentState

        Hubs { id: hubsStack }
        Company { id: company }
    }

    MouseArea {
        anchors.fill: parent
        visible: sidebar.visible
        propagateComposedEvents: true
        onClicked: {
            header.sidebarVisible = false
            mouse.accepted = false
        }
    }

    Sidebar {
        id: sidebar
        visible: header.sidebarVisible
        width: 334
        height: !notActualVersionNotification.visible ? parent.height : parent.height - header.height

        anchors {
            top: header.bottom
        }
    }

    Component.onCompleted: {
        home.forceActiveFocus()
        app.get_countries(tr.locale)
        app.check_app_version()

        if (!app.synced) {
            Popups.time_sync_popup()
        }

        __ga__.report("open", "pro page")
    }

    Connections {
        target: tr

        onTranslation_changed: {
            app.get_countries(tr.locale)
        }
    }

    Rectangle {
        id: notActualVersionNotification
        width: parent.width
        height: 50
        color: ui.colors.red1
        visible: false
        anchors {
            bottom: parent.bottom
            bottomMargin: -50
        }

        property var customDate: ""

        Custom.FontText {
            text: util.insert(tr.update_your_appication_911 + " " + tr.eol_911_version, [notActualVersionNotification.customDate])
            color: ui.colors.white
            font.pixelSize: 12
            maximumLineCount: 2
            anchors.centerIn: parent
        }

        Anime.SharinganLoader {
            id: anim
            radius: 13
            color: ui.colors.white
            useCircle: true
            visible: !updateButton.visible
            anchors {
                right: parent.right
                rightMargin: 184
                verticalCenter: parent.verticalCenter
                verticalCenterOffset: -4
            }
        }

        Item {
            width: 112
            height: 40
            anchors {
                right: parent.right
                rightMargin: 144
                verticalCenter: parent.verticalCenter
            }

            Custom.Button {
                id: updateButton
                width: parent.width
                text: tr.update_application_popup
                transparent: true
                color: ui.colors.white
                anchors.centerIn: parent
                visible: {
                    if (updater.status == "normal") return true
                    if (updater.status == "failed") return true
                    if (updater.status == "downloaded") return false
                    if (updater.status == "downloading") return false
                    if (updater.status == "installation") return false

                    return true
                }

                onClicked: {
                    updater.check_update()
                }
            }
        }

        Connections {
            target: updater

            onDownloadSuccess: {
                // notActualVersionNotification.visible = false
            }
        }

        Connections {
            target: app

            onNotActualVersion: {
                notActualVersionNotification.visible = true
                notActualVersionNotification.customDate = date
            }
        }
    }

    Connections {
        target: application

        onGoToHubNotifications: {
            var currentHubId = ""
            if (hubsStack.managementLoader.source != "") {
                currentHubId = appCompany.pro_hubs_model.current_hub ? appCompany.pro_hubs_model.current_hub.hub_id : ""
            }

            if (currentHubId != hub_id) {
                if (currentHubId) {
                    application.debug("pro -> hubs -> hub -> back to all hubs")
                    home.destroyHub()
                }

                application.debug("pro -> hubs -> dive into hub (id=" + hub_id + ")", false)
                __ga__.report("activity", "pro -> hubs -> dive into hub")

                hubsStack.startLoading()
                home.forceActiveFocus()

                appCompany.pro_hubs_model.subscribe(hub_id)
                app.hubsView.chooseHub(hub_id, appUser.cluster_user_id)
            }

            home.openOnNotificationsTab = hub_id

            app.raise_window_force()
        }
    }
}

import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13


import "qrc:/resources/qml/screens/home/header/"
import "qrc:/resources/qml/screens/home/sidebar/"
import "qrc:/resources/qml/screens/home/pages/monitoring"
import "qrc:/resources/qml/screens/home/pages/events"
import "qrc:/resources/qml/screens/home/pages/objects"
import "qrc:/resources/qml/screens/home/pages/company"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/DS/components" as DSComponents
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
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
            if (companyDataIsNotSynchronized.visible) return companyDataIsNotSynchronized.height
            return 0
        }
    }
    property var currentId: null

    property var currentIncidentsModel: appCompany.filtered_new_or_viewing_incidents_model

    property var loginTab: null

    property var currentFolder: null

    property var popup: null

    /*
    onCurrentIdChanged: {
        application.debug("TEST -> home -> currentId changed -> " + currentId)
    }

    onCurrentIncidentsModelChanged: {
        application.debug("TEST -> home -> currentIncidentsModel changed -> " + currentIncidentsModel)
    }
    */

    focus: true
    Keys.onPressed: {
        if (event.key == Qt.Key_Space) {
            app.incident_module.sound.stop()
        }
    }
    OfflinePopup {
        id: offlinePopup
        destructOnClose: false

        Connections {
            target: app
            onOnlineChanged: {
                if (app.online) {
                    application.debug("OFFLINE POPUP -> CLOSE")
                    offlinePopup.close()
                } else {
                    application.debug("OFFLINE POPUP -> OPEN")
                    offlinePopup.open()
                }
            }
        }
    }

    DS3.NavBarMain { id: navBarMain }

    Header {
        id: header

        property alias objectsStack: objectsStack

        height: __figma_46_headers_features__ ? 0 : 64

        anchors.top: navBarMain.bottom || parent.top

        visible: !navBarMain.visible
        sidebarOpenArea.onClicked: {
            header.sidebarVisible = !header.sidebarVisible
        }

        Connections {
            target: application

            onNotificationClicked: {
                header.currentState = 1
                eventsStack.eventsSidebar.notificationClicked()
            }
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

        Monitoring {}
        Events { id: eventsStack }
        Objects { id: objectsStack }
        Company { id: company }
        Rectangle { color: ui.colors.black }
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

        property alias objectsStack: objectsStack
    }

    Connections {
        target: app.company_module

        onCompanyDeleted: {
            app.login_module.login_into_personal_account()
        }
    }

    Component.onCompleted: {
        home.forceActiveFocus()
        app.get_countries(tr.locale)
        app.check_app_version()

        if (!app.synced) {
            Popups.time_sync_popup()
        }

        __ga__.report("open", "company page")
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
            target: app

            onNotActualVersion: {
                notActualVersionNotification.visible = true
                notActualVersionNotification.customDate = date
            }
        }
    }

    DSComponents.CompanyDataIsNotSynchronized {
        id: companyDataIsNotSynchronized

        anchors {
            bottom: home.bottom
            bottomMargin: -height
        }

        visible: !notActualVersionNotification.visible
                 && companyAccess.COMPANY_GENERAL_INFO_EDIT
                 && !appCompany.data.synchronized
                 && !company.editModeOpened

        onEntered: {
            header.currentState = 3
            sidebar.openCompany()
            company.editModeOpen()
        }
    }

    Connections {
        target: app

        onCompanyHubPermissionDurationReceived: (data) => {
            if (!!data) DesktopPopups.popupByPath(
                "qrc:/resources/qml/components/911/DS3/popups/InstallerRequestedAccessPopup.qml", {
                    companyExpirationTimestamp: data.expirationTimestamp,
                    installerName: [data.additional_data.first_name, data.additional_data.last_name].join(" "),
                    requestedHours: data.additional_data.permanent
                        ? "PERMANENT"
                        : data.additional_data.temporary.duration.seconds / 3600,
                    requestId: data.additional_data.permission_request_id,
                    isPermanentCompanyAccess: data.permissionType == "FULL_PERMISSION" && data.expirationTimestamp == 0
                }
            )
        }
    }
}

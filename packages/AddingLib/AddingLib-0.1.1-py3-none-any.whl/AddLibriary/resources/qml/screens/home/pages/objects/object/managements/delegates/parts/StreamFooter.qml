import QtQuick 2.12
import QtQuick.Controls 2.13
import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
    id: streamFooter

    property bool cancelBinding: false
    property var companyPhodAccess: device.company_phod_access
    property bool showFooter: {
        if (!device) return false
        if (!appUser.company_id) { // Owner
            if (!hub.access_to_camera_privacy_settings_allowed) {  // old hub
                return hub.current_user.cameras_access
            } else {
                return !device.stream_access_denied && hub.access_to_camera_privacy_settings_allowed
            }
        }
        if (!__phod_company_features__) return false  // Employee
        return !device.stream_access_denied
    }


    width: parent.width
    height: {
        if (!showFooter) return 0
        Math.max(buttonTitle.height, streamButton.height) + 16
    }

    anchors {
        horizontalCenter: parent.horizontalCenter
        bottom: parent.bottom
    }

    visible: showFooter

    Rectangle {
        width: parent.width - 32
        height: showFooter ? 1 : 0

        anchors.horizontalCenter: parent.horizontalCenter

        color: list.currentIndex == index ? ui.ds3.bg.highest : deviceDelegate.selectedColor
    }

    DS3.AtomTitle {
        id: buttonTitle

        anchors {
            left: parent.left
            leftMargin: 16
            right: streamButton.left
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        title: tr.view_camera_now
    }

    DS3.ButtonMini {
        id: streamButton

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/views_icons/Start-S.svg"
        enabled: device.online
        opacity: enabled ? 1 : 0.3

        onClicked: {
            if (device.online) {
                app.hub_management_module.open_camera_stream(hub, device)
            }
        }
    }
}
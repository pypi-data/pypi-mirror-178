import QtQuick 2.12
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

// This element has children: UserRegular, UserNavigation, UserSelectionMulti, UserSelectionSingle, UserSwitch
Rectangle {
    id: masterUser

//  Image of the user
    property alias imageSource: image.source
//  AtomTitle component
    property alias atomTitle: atomTitle
//  User role
    property var role: ""
//  User has privacy officer badge
    property var hasPrivacyOfficerBadge: false

    implicitWidth: parent.width
    implicitHeight: Math.max(64, atomTitle.height + 24)

    color: ui.ds3.figure.transparent

    DS3.Image {
        id: defaultImage

        anchors.fill: image

        source: {
            if (role == tr.pro) return "qrc:/resources/images/Athena/user_rows/ProUserPlaceholderImage-M.svg"
            return "qrc:/resources/images/Athena/user_rows/UserPlaceholderImage-M.svg"
        }
        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
        visible: image.status != Image.Ready
    }

    DS3.Image {
        id: image

        width: 40
        height: 40

        anchors {
            left: parent.left
            leftMargin: 16
            top: parent.top
            topMargin: 12
        }

        layer.enabled: true
        layer.effect: OpacityMask { maskSource: circle }
    }

    Rectangle {
        id: circle

        anchors.fill: image

        radius: width / 2
        visible: false
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: parent.left
            leftMargin: 72
            right: parent.right
            rightMargin: 48
            verticalCenter: parent.verticalCenter
        }

        badge: role
        badgeColor: {
            if (role == tr.pro) return ui.ds3.figure.warningContrast
            if (role == tr.admin) return ui.ds3.figure.positiveContrast
            return ui.ds3.figure.secondary
        }
    }


    Item {
        id: privacyOfficerBadgeItem

        width: 14
        height: 14

        anchors {
            left: parent.left
            leftMargin: 42
            top: parent.top
            topMargin: 42
        }

        visible: hasPrivacyOfficerBadge

        Rectangle {
            radius: width / 2
            color: ui.ds3.bg.highest
            anchors.fill: parent
        }

        Image {
            id: yellowStarImage

            anchors.centerIn: parent

            sourceSize.width: 12
            sourceSize.height: 12

            source: "qrc:/resources/images/Athena/common_icons/PrivacyOfficer-M.svg"
        }
    }
}

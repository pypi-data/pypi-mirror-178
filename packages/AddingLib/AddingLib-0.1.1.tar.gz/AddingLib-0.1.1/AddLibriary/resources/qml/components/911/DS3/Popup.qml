import QtQuick 2.13
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3" as DS3


// Popup that contains cross button and any information placed inside column
Popup {
    id: popup

//  Title of the popup
    property var title: ""
//  Whether to destruct component after closing. Preferrably do not change
    property bool destructOnClose: true
//  Visibility of cross button
    property bool hasCrossButton: true
//  Margins around the content
    property var sideMargins: 24
//  Callback on enter key pressed
    property var enterOrReturnedPressedCallback
//  Callback on backspace key pressed
    property var backspacePressedCallback
//  Background color
    property alias backgroundColor: popupContainer.color
//  Background color of default NavBarModal header
    property var defaultHeaderBackgroundColor: ui.ds3.figure.transparent
//  Header component
    property Component header: defaultHeaderComponent
//  Footer component
    property Component footer: defaultFooterComponent
//  Main scroll view
    property alias contentView: contentView
//  Readonly header item
    readonly property alias headerItem: headerItem.item
//  Readonly footer item
    readonly property alias footerItem: footerItem.item
//  Components that should be placed inside content container
    default property alias content: contentContainer.data
//  Contant default policy for cases when you need to change from it and back
    readonly property var defaultPolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    /* -------------------------------------------- */
    /* desktop tests */
    property var accessibleHeaderIcoName: ""
    property var accessibleHeaderTextName: ""
    property var accessibleHeaderAreaName: ""
    property var accessibleHeaderAreaDescription: ""
    /* -------------------------------------------- */

    width: 300

    anchors.centerIn: parent

    parent: ApplicationWindow.contentItem
    modal: true
    focus: true
    padding: 0
    closePolicy: defaultPolicy
    enter: Transition {
        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 200 }
    }
    exit: Transition {
        NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 200 }
    }
    background: Rectangle {
        color: ui.ds3.bg.overlay
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    onAboutToShow: {
    }

    onAboutToHide: {
    }

    onClosed: {
        if (destructOnClose) {
             popup.destroy()
        } else {
            heightAnimation.enabled = false
        }
    }

    onOpened: {
        heightAnimation.enabled = true
    }

    Component.onCompleted: {
        // If popup height has not been initialized. Then set height based on the content
        if (height == 0) {
            contentView.height = Qt.binding(
                () => Math.min(contentView.contentHeight, application.height - footerItem.height - headerItem.height - 64)
            )
            popupContainer.height = Qt.binding(() => headerItem.height + contentView.height + footerItem.height)
            height = Qt.binding(() => popupContainer.height)
        // Else set content height based on the popup height
        } else {
            contentView.height = Qt.binding(() => height - footerItem.height - headerItem.height)
        }
    }

    Component {
        id: defaultHeaderComponent

        DS3.NavBarModal {
            backgroundColor: defaultHeaderBackgroundColor
            showCloseIcon: hasCrossButton
            headerText: title

            /* -------------------------------------------- */
            /* desktop tests */
            accessibleIcoName: popup.accessibleHeaderIcoName
            accessibleTextName: popup.accessibleHeaderTextName
            accessibleAreaName: popup.accessibleHeaderAreaName
            accessibleAreaDescription: popup.accessibleHeaderAreaDescription
            /* -------------------------------------------- */
        }
    }

    Component {
        id: defaultFooterComponent

        Item {
            width: parent.width
            height: 24
        }
    }

    Rectangle {
        id: roundedMask

        width: popupContainer.width
        height: popupContainer.height

        visible: false
        radius: 12
        layer.enabled: true
    }

    contentItem: Rectangle {
        id: popupContainer

        width: parent.width
        height: headerItem.height + contentView.height + footerItem.height

        color: ui.ds3.bg.base
        clip: true
        layer.enabled: true
        layer.samplerName: "maskSource"
        layer.effect: ShaderEffect {
            property var colorSource: roundedMask
            property real contentWidth: popup.width
            property real contentHeight: popup.height

            //fragmentShader: util.shaders.round_corners
        }

        Behavior on height {
            id: heightAnimation

            enabled: false

            NumberAnimation {
                duration: 200
            }
        }

        Loader {
            id: headerItem

            anchors {
                left: parent.left
                right: parent.right
                top: parent.top
            }

            sourceComponent: header
            z: 2
        }

        DS3.ScrollView {
            id: contentView

            width: parent.width

            anchors {
                fill: undefined
                top: headerItem.bottom
            }

            padding: 0
            z: 1

            Column {
                id: contentContainer

                anchors {
                    left: parent.left
                    right: parent.right
                    margins: sideMargins
                }
            }
        }

        Loader {
            id: footerItem

            anchors {
                left: parent.left
                right: parent.right
                bottom: parent.bottom
            }

            sourceComponent: footer
            z: 2
        }

        Keys.onPressed: {
            if (!!enterOrReturnedPressedCallback && [Qt.Key_Return, Qt.Key_Enter].includes(event.key)) {
                enterOrReturnedPressedCallback()
            }
            else if (!!backspacePressedCallback && Qt.Key_Backspace == event.key) {
                backspacePressedCallback()
            }
        }
    }

    Component.onDestruction: {
        popup.close()
        modal = false
    }

    Connections {
        target: app.login_module

        onLogoutSignal: {
            popup.close()
        }
    }
}

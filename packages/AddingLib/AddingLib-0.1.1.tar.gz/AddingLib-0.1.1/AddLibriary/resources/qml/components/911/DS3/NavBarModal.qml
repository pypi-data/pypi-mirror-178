import QtQuick 2.7
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: navBarModal

//  Title of the screen
    property var headerText: ''
//  Property defining rounding
    property var isRound: true
//  Whether to show the back arrow
    property var showBackArrow: false
//  Enabled prop for back arrow
    property alias backArrowEnabled: backIcon.enabled
//  Whether to show manual icon
    property var showManualIcon: false
//  Whether to show close icon
    property var showCloseIcon: true
//  Whether to show text on the left side
    property bool isNavigationTextLeft: false
//  Text pf navigation button
    property var navigationText: ""
//  On close icon clicked
    property var onClosed: () => {
        popup.close()
    }
//  Manual icon on the right flag
    property bool isManualIconRight: !showCloseIcon
//  Color of the component
    property color backgroundColor: ui.ds3.bg.high
//  On back arrow clicked
    signal backAreaClicked
//  On manual icon clicked
    signal manualAreaClicked
//  On navigation text clicked
    signal navigationTextClicked

    /* -------------------------------------------- */
    /* desktop tests */
    property var accessibleIcoName: ""
    property var accessibleTextName: ""
    property var accessibleAreaName: ""
    property var accessibleAreaDescription: ""
    /* -------------------------------------------- */

    width: parent.width
    height: 56

    anchors {
        top: parent.top
        horizontalCenter: parent.horizontalCenter
    }

    // Fix performance problems. Use OpacityMask for background instead of top-level.
    Rectangle {
        anchors.fill: parent

        color: backgroundColor
        // creates roundness for the upper corners
        layer.enabled: isRound
        layer.effect: OpacityMask {
            maskSource: Item {
                width: navBarModal.width
                height: navBarModal.height

                Rectangle {
                    anchors {
                        fill: parent
                        bottomMargin: -12
                    }

                    radius: 12
                }
            }
        }
    }

    DS3.ButtonIcon {
        id: backIcon

        anchors {
            left: parent.left
            leftMargin: 16
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/Back-M.svg"
        visible: showBackArrow
        opacity: enabled ? 1 : 0.3

        onClicked: backAreaClicked()
    }

    DS3.Text {
        width: parent.width

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: showBackArrow || showCloseIcon || showManualIcon ? 56 : 16
            right: parent.right
            rightMargin: showBackArrow || showCloseIcon || showManualIcon ? 56 : 16
        }

        text: headerText
        style: ui.ds3.text.title.XSRegular
        horizontalAlignment: Text.AlignHCenter
        hasElide: true

        /* ------------------------------------------------ */
        /* desktop tests */
        Accessible.name: navBarModal.accessibleTextName
        Accessible.description: text
        Accessible.role: Accessible.Paragraph
        /* ------------------------------------------------ */
    }

    DS3.ButtonIcon {
        id: manualIcon

        anchors {
            verticalCenter: parent.verticalCenter
            left: isManualIconRight ? undefined : parent.left
            right: isManualIconRight ? parent.right : undefined
            leftMargin: !isManualIconRight ? showBackArrow ? 48 : 16 : 0
            rightMargin: isManualIconRight ? showCloseIcon ? 48 : 16 : 0
        }

        source: "qrc:/resources/images/Athena/common_icons/icon_tutorial.svg"
        visible: showManualIcon
        opacity: enabled ? 1 : 0.3

        onClicked: manualAreaClicked()
    }

    DS3.ButtonIcon {
        id: closeIcon

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        visible: showCloseIcon
        source: "qrc:/resources/images/Athena/common_icons/Cross-M.svg"
        opacity: enabled ? 1 : 0.3
        
        onClicked: {
            onClosed()
        }

        /* -------------------------------------------- */
        /* desktop tests */
        Accessible.name: navBarModal.accessibleIcoName
        Accessible.description: "<button enabled=" + Accessible.checkable + ">" + source + "</button>"
        Accessible.role: Accessible.Button
        Accessible.checkable: visible && enabled
        Accessible.onPressAction: {
            if (!Accessible.checkable) return
            closeIcon.clicked(true)
        }
        /* -------------------------------------------- */
    }

    DS3.Text {
        text: navigationText
        color: ui.ds3.figure.interactive
        style: ui.ds3.text.body.MRegular

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 16
        }

        visible: isNavigationTextLeft

        DS3.MouseArea {
            onClicked: navigationTextClicked()
        }
    }

    /* ---------------------------------------------------- */
    /* desktop tests */
    Accessible.name: navBarModal.accessibleAreaName
    Accessible.description: navBarModal.accessibleAreaDescription
    Accessible.role: Accessible.Grouping
    /* ---------------------------------------------------- */
}

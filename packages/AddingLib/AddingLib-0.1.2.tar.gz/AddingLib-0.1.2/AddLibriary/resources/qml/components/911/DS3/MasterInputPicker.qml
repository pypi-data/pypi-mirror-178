import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


ComboBox {
    id: inputPicker

//  default text when current index is -1
    property var defaultText: tr.a911_not_chosen + "..."
//  Input element for regex and atomInput customization
    property alias input: input
//  Use this for adding suffix
    property string suffix: ""
//  Width of the sheet action part
    property var sheetActionWidth: Math.max(inputPicker.width, 200)
//  Custom highlighted index for focus on suggestion
    property var customHighlightedIndex: inputPicker.highlightedIndex
//  Height of the delegate item
    readonly property real delegateHeight: 40
    property var notIncludedErrorText: ""

    property var onInputTextChanged: () => {}
    property var onPickerActivated: () => {}
    property var onInputActiveFocusChanged: () => {}

    function scrollToIndex(bestMatch) {
        customHighlightedIndex = bestMatch
        let moveTo = delegateHeight * bestMatch
        scrollView.scrollBar.scrollAnimation.stop()
        scrollView.scrollBar.scrollTo(moveTo)
    }

    // a quick solution to get rid of binding
    Component.onCompleted: {
        customHighlightedIndex = inputPicker.highlightedIndex
    }

    Keys.onPressed: {
        if (event.key == Qt.Key_Up) {
            if (customHighlightedIndex > 0) {
                customHighlightedIndex -= 1
                // scrollToIndex(customHighlightedIndex)
            }
        }
        if (event.key == Qt.Key_Down) {
            if (customHighlightedIndex + 1 < inputPicker.count) {
                customHighlightedIndex += 1
                // scrollToIndex(customHighlightedIndex)
            }
        }
    }

    height: contentItem.height

    model: []
    currentIndex: -1
    editable: true

    delegate: ItemDelegate {
        id: itemDelegate

        width: sheetActionWidth
        height: delegateHeight

        Rectangle {
            anchors.fill: parent

            color: customHighlightedIndex == index ? ui.ds3.bg.high : ui.ds3.bg.highest
        }

        contentItem: DS3.Text {
            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 16
            }

            style: ui.ds3.text.body.MRegular
            text: suffix ? modelData + suffix : modelData
            hasElide: true
            rightPadding: 30
        }

        DS3.Icon {
            anchors {
                right: parent.right
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            visible: inputPicker.currentIndex == index
            source: "qrc:/resources/images/Athena/common_icons/Shape.svg"
        }

        DS3.MouseArea {
            acceptedButtons: Qt.NoButton

            onContainsMouseChanged: {
                if (containsMouse) {
                    customHighlightedIndex = index
                }
            }
        }
    }

    indicator: Item {}

    contentItem: Item {
        height: input.height
        width: parent.width

        DS3.InputSingleLine {
            id: input

            anchors {
                left: parent.left
                right: parent.right
                leftMargin: 0
                rightMargin: 0
            }

            hasValidationOnFocusLost: true
            color: atomInput.activeFocus || popup.visible ? ui.ds3.bg.high : ui.ds3.bg.highest

            atomInput {
                required: false
                labelItem.hasElide: true

                onActiveFocusChanged: onInputActiveFocusChanged()
                onTextEdited: onInputTextChanged()
            }
        }
    }

    background: Rectangle {
        color: ui.ds3.bg.highest
    }


    popup: Popup {
        id: popup

        width: sheetActionWidth
        height: popup.visible ? Math.min(contentItem.implicitHeight, delegateHeight * 7.5) : 0

        padding: 0
        y: inputPicker.height + 1

        contentItem: DS3.ScrollView {
            id: scrollView

            width: sheetActionWidth

            padding: 0

            ListView {
                id: contentList

                width: sheetActionWidth
                implicitHeight: contentHeight

                clip: true
                spacing: 1
                model: inputPicker.popup.visible ? inputPicker.delegateModel : null
                currentIndex: customHighlightedIndex
                interactive: false
            }

            Rectangle {
                id: roundedMask

                width: bgRectangle.width
                height: bgRectangle.height

                visible: false
                radius: 12
                layer.enabled: true
            }

            layer.enabled: true
            layer.samplerName: "maskSource"
            layer.effect: ShaderEffect {
                property var colorSource: roundedMask
                property real contentWidth: popup.width
                property real contentHeight: popup.height

               // fragmentShader: util.shaders.round_corners
            }
        }

        background: Rectangle {
            id: bgRectangle

            width: sheetActionWidth

            color: ui.ds3.bg.high
            radius: 12

            DropShadow {
                anchors.fill: back

                verticalOffset: 1
                radius: parent.radius
                samples: 30
                color: ui.ds3.bg.overlay
                source: back
            }

            Rectangle {
                id: back

                anchors.fill: parent

                color: ui.ds3.bg.base
                radius: 12
            }
        }

        onAboutToHide: {
            input.forceActiveFocus()
        }
    }

    onActivated: onPickerActivated()
}

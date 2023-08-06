import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    id: popup

//  Text of the popup
    property alias text: textLabel.text
//  When dialog has two vertical buttons
    property bool isVertical: false
//  First button callback
    property var firstButtonCallback: () => {}
//  Second button callback
    property var secondButtonCallback: () => {}
//  First button text
    property alias firstButtonText: firstButton.text
//  Second button text
    property alias secondButtonText: secondButton.text
//  Set button color
    property bool isFirstButtonRed: false
    property bool isSecondButtonRed: false
//  When dialog has input
    property bool isInput: false
//  First button callback (with input)
    property var inputValueHandler: (value) => {}
//  Atom input
    property alias inputFieldAtomInput: inputField.atomInput
//  input field
    property alias inputField: inputField
//  When first button without border
    property alias firstButtonHasBorder: firstButton.hasBorder
//  When second button without border
    property alias secondButtonHasBorder: secondButton.hasBorder
//  When fist button is outlined
    property alias firstButtonIsOutline: firstButton.isOutline
//  When second button is outlined
    property alias secondButtonIsOutline: secondButton.isOutline
//  For changing first button
    property alias firstButton: firstButton
//  For changing second button
    property alias secondButton: secondButton
//  Property which allows closing by default
    property bool autoClose: true
//  Property which switch on Spinner
    property bool isLoading: false
//  Spinner item instead of first button
    property alias spinnerItem: spinnerItem

    width: 500

    hasCrossButton: false

    header: Item {
        width: parent.width
        height: Math.max(titleItem.height + titleItem.anchors.topMargin, 32)

        DS3.Text {
            id: titleItem

            width: parent.width - 2 * 24

            anchors {
                top: parent.top
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }

            style: ui.ds3.text.title.XSBold
            horizontalAlignment: Text.AlignHCenter
            text: !!popup ? popup.title : ""

            Binding on height {
                when: !titleItem.text
                value: 0
            }
        }
    }

    DS3.Spacing {
        height: 8
    }

    Item {
        width: parent.width
        height: textLabel.contentHeight

        DS3.Text {
            id: textLabel

            width: parent.width

            text: !!popup ? popup.text : ""
            style: ui.ds3.text.body.MRegular
            horizontalAlignment: Text.AlignHCenter

            Rectangle {
                id: backgroundText

                anchors.fill: parent

                color: ui.ds3.bg.accent
                opacity: 0.5
                visible: false
            }

            ToolTip {
                id: tooltip

                contentItem: DS3.Text {
                    text: tr.copied
                    style: ui.ds3.text.body.SRegular
                    color: ui.ds3.bg.accent
                }

                background: Rectangle {
                    color: ui.ds3.bg.low
                    radius: 4
                    border {
                        width: 1
                        color: ui.ds3.figure.interactive
                    }
                }
            }

            MouseArea {
                anchors.fill: parent

                visible: __debug__

                onClicked: {
                    util.set_clipboard_text(textLabel.text)
                    tooltip.show("", 500)
                }

                onPressed: {
                    backgroundText.visible = true
                }

                onExited: {
                    backgroundText.visible = false
                }
            }
        }
    }

    DS3.Spacing {
        height: 12

        visible: isInput
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.InputPassword {
            id: inputField

            visible: isInput
            isPasswordField: false
        }
    }

    DS3.Spacing {
        height: 48
    }

    GridLayout {
        width: parent.width

        flow: isVertical ? GridLayout.TopToBottom : GridLayout.LeftToRight
        layoutDirection: Qt.RightToLeft
        rowSpacing: 8
        columnSpacing: 16

        Item {
            id: firstButtonContainer

            Layout.fillWidth: true
            Layout.preferredWidth: 1
            Layout.preferredHeight: firstButton.height

            DS3.ButtonContained {
                id: firstButton

                width: parent.width

                text: tr.ok
                visible: !isLoading
                isAttention: isFirstButtonRed

                onClicked: {
                    inputValueHandler(inputField.atomInput.text)
                    firstButtonCallback()
                    if (autoClose) popup.close()
                }
            }

            DS3.ButtonProgress {
                id: spinnerItem

                anchors.centerIn: parent

                visible: isLoading
            }
        }

        DS3.ButtonOutlined {
            id: secondButton

            Layout.fillWidth: true
            Layout.preferredWidth: 1
            Layout.preferredHeight: height

            visible: !!text
            isOutline: true
            isAttention: isSecondButtonRed

            onClicked: {
                secondButtonCallback()
                if (autoClose) popup.close()
            }
        }
    }
}
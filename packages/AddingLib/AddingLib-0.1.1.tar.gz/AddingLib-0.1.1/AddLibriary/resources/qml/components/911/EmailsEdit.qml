import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: plusMinusItem
    color: "transparent"
    border.color: "white"
    border.width: 0
    width: 400
    height: keyText.contentHeight + listView.contentHeight + distance

    property var key: ""
    property var model: []
    property var maxPhoneNumbers: 0
    property var error: false
    property var distance: 6
    property alias keyText: keyText
    property alias listView: listView
    signal errorsResult(variant result)

    Custom.FontText {
        id: keyText
        text: parent.key
        width: parent.width
        color: ui.colors.white
        opacity: 0.5
        font.pixelSize: 14
        font.weight: Font.Light
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignLeft
        anchors {
            top: parent.top
            left: parent.left
        }
    }

    ListView {
        id: listView
        width: parent.width
        spacing: plusMinusItem.distance - 4
        interactive: false
        anchors {
            top: keyText.bottom
            topMargin: model.length > 0 ? distance + 4 : 4
            left: parent.left
            bottom: parent.bottom
        }

        delegate: Custom.TextField {
            id: delegate
            width: parent.width
            control.text: modelData.email
            placeHolderText: ""
            control.rightPadding: 48
            control.maximumLength: 100

            Image {
//                visible: listView.model.length > 1
                sourceSize.width: 40
                sourceSize.height: 40
                width: 24
                height: 24
                source: "qrc:/resources/images/icons/control-a-minus-button.svg"
                anchors {
                    verticalCenter: delegate.background.verticalCenter
                    right: parent.right
                    rightMargin: 8
                }

                Custom.HandMouseArea {
                    onClicked: {
                        var listViewVar = listView
                        var indexVar = index
                        focus = true
                        listViewVar.model = listViewVar.model.slice(0, indexVar).concat(listViewVar.model.slice(indexVar + 1, listViewVar.model.length))
                    }
                }
            }
            Connections {
                target: plusMinusItem
                onErrorsResult: {
                    var editObjectNum = `5[${index}].1`
                    var facilityNum = `2.5[${index}].1`

                    if (!result[facilityNum] && !result[editObjectNum])
                        return

                    plusMinusItem.error = true
                    delegate.valid = false

                    if (result[editObjectNum])
                        delegate.error = result[editObjectNum].message
                    else
                        delegate.error = result[facilityNum].message
                }
            }

            control.onEditingFinished: {
                var newEmail = {"email": control.text}
                listView.model = listView.model.slice(0, index).concat(newEmail, listView.model.slice(index + 1, listView.model.length))
            }
        }

        footer: Item {
            visible: (maxPhoneNumbers == 0) ? true : (maxPhoneNumbers > listView.model.length)
            width: parent.width
            height: visible ? 40 + plusMinusItem.distance - 4 : 1

            Rectangle {
                width: parent.width
                height: 40
                radius: height / 2
                color: ui.colors.dark1
                anchors.bottom: parent.bottom

                Image {
                    sourceSize.width: 40
                    sourceSize.height: 40
                    width: 24
                    height: 24
                    source: "qrc:/resources/images/icons/control-a-plus-button.svg"
                    anchors.centerIn: parent

                    Custom.HandMouseArea {
                        onClicked: {
                            focus = true
                            var newEmail = {"email": ""}
                            listView.model = listView.model.concat([newEmail])
                        }
                    }
                }
            }
        }

        Component.onCompleted: {
            listView.model = plusMinusItem.model
        }
    }
}
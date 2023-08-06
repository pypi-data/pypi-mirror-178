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
    property var withType: true
    property var maxPhoneNumbers: 0
    property var error: false
    property var distance: 6
    property alias keyText: keyText
    property alias listView: listView
//     gbr phones field is optional
    property var emptyField: false
    property var phonesAreNotEmpty: false
    signal errorsResult(variant result)

    function checkPhonesForEmptiness() {
        var emptyPhonesExist = false
        for(var child in listView.contentItem.children) {
            if (listView.contentItem.children[child]["objectName"] == "delegate"
                && listView.contentItem.children[child].control.text.length == 0) {
                emptyPhonesExist = true
                break
            }
        }
        phonesAreNotEmpty = !emptyPhonesExist
    }

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
            objectName: "delegate"
            width: parent.width
            control.text: modelData.number
            placeHolderText: ""
            control.rightPadding: 48
            control.validator: RegExpValidator { regExp: /(\+|[0-9])?[0-9]+/ }
            control.maximumLength: 30
            Connections {
                target: plusMinusItem
                onErrorsResult: {
                    var empliyeeNum = `4[${index}].1`
                    var facilityNum = `2.4[${index}].1`
                    var gbrNum = `7[${index}].1`
                    var responciblePersonNum = `9[${index}].1`

                    if (result[empliyeeNum]) {
                        delegate.valid = false
                        delegate.error = result[empliyeeNum].message
                    }
                    if (result[facilityNum]) {
                        delegate.valid = false
                        plusMinusItem.error = true
                        delegate.error = result[facilityNum].message
                    }
                    if (result[gbrNum]) {
                        delegate.valid = false
                        delegate.error = result[gbrNum].message
                    }
                    if (result[responciblePersonNum]) {
                        delegate.valid = false
                        delegate.error = result[responciblePersonNum].message
                    }
                }
            }

            Image {
                visible: plusMinusItem.emptyField ? listView.model.length > 0 : listView.model.length > 1
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
                        plusMinusItem.checkPhonesForEmptiness()
                        var listViewVar = listView
                        var indexVar = index
                        focus = true
                        listViewVar.model = listViewVar.model.slice(0, indexVar).concat(listViewVar.model.slice(indexVar + 1, listViewVar.model.length))
                    }
                }
            }

            control.onTextEdited: checkPhonesForEmptiness()

            control.onEditingFinished: {
                var newNumber = plusMinusItem.withType ? {"number": control.text, "type": modelData.type} : {"number": control.text}
                listView.model = listView.model.slice(0, index).concat(newNumber, listView.model.slice(index + 1, listView.model.length))
            }

            control.onActiveFocusChanged: {
                var newNumber = plusMinusItem.withType ? {"number": control.text, "type": modelData.type} : {"number": control.text}
                listView.model = listView.model.slice(0, index).concat(newNumber, listView.model.slice(index + 1, listView.model.length))
            }

            Component.onCompleted: {
                var newNumber = plusMinusItem.withType ? {"number": control.text, "type": modelData.type} : {"number": control.text}
                listView.model = listView.model.slice(0, index).concat(newNumber, listView.model.slice(index + 1, listView.model.length))
                checkPhonesForEmptiness()
            }
        }

        footer: Item {
            visible: (maxPhoneNumbers == 0) ? true : (maxPhoneNumbers > listView.model.length)
            width: parent.width
            height: visible ? 40 + plusMinusItem.distance - 4: 1

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
                            var newNumber = plusMinusItem.withType ? {"number": "", "type": "MAIN"} : {"number": ""}
                            listView.model = listView.model.concat([newNumber])
                            phonesAreNotEmpty = false
                        }
                    }
                }
            }
        }

        Component.onCompleted: {
            if (plusMinusItem.model.length == 0) {
                if (plusMinusItem.emptyField) {
                   plusMinusItem.model = []
                } else {
                    var newNumber = plusMinusItem.withType ? {"number": "", "type": "MAIN"} : {"number": ""}
                    plusMinusItem.model = plusMinusItem.model.concat([newNumber])
                }
            }
            listView.model = plusMinusItem.model
        }
    }
}
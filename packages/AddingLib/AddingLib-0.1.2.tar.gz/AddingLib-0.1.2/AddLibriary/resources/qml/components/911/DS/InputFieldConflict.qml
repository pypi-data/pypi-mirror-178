import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/" as Desktop
import "qrc:/resources/qml/components/911/DS" as DS


// Component that used when data conflict resolving are neccessary
Item {
    id: inputFieldConflict

//  Conflict data, from which user will choose correct items
    property var conflictData: []
//  Key that holds the conflict value in the conflictData ('key' if cnoflictData = [{'key': 'conflictValue'}]
//  Keep it undefined, conflictData is plain array
    property string valueKey
//  Name of the property, that will be shown in conflict popup
    property string propertyName
//  Info that places below the conflict field
    property alias info: infoItem.text
//  Title of the conflict popup
    property alias conflictTitle: conflictTitle.text
//  Info of the conflict popup
    property alias conflictInfo: conflictInfo.text

//  Conflict has been resolved and desirable values have been selected
    signal selected(var values)

    width: 400
    height: content.height

    Column {
        id: content

        width: parent.width

        spacing: 8

        DS.Text {
            text: propertyName

            size: 14
            line: 20
            color: ui.colors.secondary
        }

        Rectangle {
            id: fieldStub

            width: parent.width
            height: 40
            color: ui.backgrounds.highest

            radius: 8
            border {
                color: ui.colors.warningContrast
                width: 1
            }

            DS.MouseArea {
                onClicked: popup.open()
            }

            DS.ButtonRound {
                anchors {
                    left: fieldStub.right
                    leftMargin: 8
                    verticalCenter: fieldStub.verticalCenter
                }

                style: ui.controls.alarm

                onClicked: popup.open()
            }
        }

        DS.Text {
            id: infoItem

            width: parent.width
            height: text ? contentHeight : 0

            size: 14
            line: 20
            color: ui.colors.nonessential
        }
    }

    Desktop.AjaxPopup {
        id: popup

        width: 328
        height: popupContent.height

        anchors.centerIn: parent

        destructOnClose: false
        closePolicy: Popup.NoAutoClose

        contentItem: Rectangle {
            radius: 8
            color: ui.backgrounds.base

            anchors.fill: parent

            ButtonRound {
                z: 10

                anchors {
                    right: parent.right
                    top: parent.top
                    margins: 16
                }

                side: 32
                style: ui.controls.cross

                onClicked: popup.close()
            }

            Column {
                id: popupContent

                width: parent.width - 64

                anchors.horizontalCenter: parent.horizontalCenter

                DS.Spacing { height: 32 }

                DS.Text {
                    id: conflictTitle

                    width: parent.width - 48

                    anchors.horizontalCenter: parent.horizontalCenter

                    color: ui.colors.base
                    size: 16
                    line: 24
                    horizontalAlignment: Text.AlignHCenter
                }

                DS.Spacing { height: 4 }

                DS.Text {
                    id: conflictInfo

                    width: parent.width

                    color: ui.colors.secondary
                    size: 12
                    line: 16
                    horizontalAlignment: Text.AlignHCenter
                }

                DS.Spacing { height: 32 }

                DS.Text {
                    width: parent.width

                    text: propertyName
                    color: ui.colors.secondary
                    size: 14
                    line: 20
                    horizontalAlignment: Text.AlignHCenter
                }

                DS.Spacing { height: 20 }

                ListView {
                    id: selectionList

                    property var selectedValues: []
                    property var checkedCounter: 0

                    implicitWidth: contentItem.childrenRect.width
                    height: contentHeight

                    anchors.horizontalCenter: parent.horizontalCenter

                    model: conflictData
                    spacing: 16
                    delegate: DS.Checkbox {
                        id: checkboxDelegate

                        maxWidth: popupContent.width

                        text: valueKey ? modelData[valueKey] : modelData

                        onCheckedChanged: selectionList.checkedCounter += checked ? 1 : -1
                        enabled: selectionList.checkedCounter < 5 || checked
                    }
                }

                DS.Spacing { height: 64 }

                DS.ButtonRegular {
                    anchors.horizontalCenter: parent.horizontalCenter

                    enabled: selectionList.checkedCounter > 0
                    text: tr.select_button

                    onClicked: {
                        var selectedValuesList = []

                        for (var index in selectionList.model) {
                            if (selectionList.itemAtIndex(index).checked) selectedValuesList.push(selectionList.model[index])
                        }

                        selected(selectedValuesList)
                        popup.close()
                    }
                }

                DS.Spacing { height: 32 }

                ButtonGroup {
                    id: buttonGroup
                }
            }
        }
    }
}

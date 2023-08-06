import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: settingsSelection

//  List of chosen days
    property var checkedDays: []
//  Whether to cancel property binding
    property bool cancelBinding: true

    Component.onCompleted: if (cancelBinding) checkedDays = checkedDays

    width: parent.width
    height: 64

    color: ui.ds3.bg.highest

    Row {
        anchors.centerIn: parent

        spacing: 16

        Repeater {
            width: parent.width

            model: [
                tr.schedule_monday_short,
                tr.schedule_tuesday_short,
                tr.schedule_wednesday_short,
                tr.schedule_thursday_short,
                tr.schedule_friday_short,
                tr.schedule_saturday_short,
                tr.schedule_sunday_short,
            ]

            delegate: DS3.CheckBoxRound {
                id: roundButton

                isOutline: !checkedDays.includes(index == 6 ? 0 : index + 1)
                text: modelData.slice(0, 3)

                onClicked: {
                    let day_index = index == 6 ? 0 : index + 1
                    roundButton.isOutline ? checkedDays.push(day_index) : checkedDays.splice(checkedDays.indexOf(day_index), 1)
                    roundButton.isOutline = !roundButton.isOutline
                    checkedDays.sort((function(a, b) {
                      return a - b;
                    }))
                    checkedDaysChanged()
                }
            }
        }
    }
}
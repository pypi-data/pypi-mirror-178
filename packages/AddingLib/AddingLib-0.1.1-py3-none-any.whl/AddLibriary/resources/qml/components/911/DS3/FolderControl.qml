import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
// a model for the folder control
    default property alias model: row.model
// current index to track which folder is selected
    property int currentIndex: 0

//  when current index changes this signal is emitted with the index that should become current
    signal currentIndexDiffer (int index)

    width: parent.width
    height: 40

    color: ui.ds3.bg.high

    Row {
        anchors {
            fill: parent
            leftMargin: 16
        }

        Repeater {
            id: row

            delegate: DS3.Folder {
                labelText: modelData.text
                selected: currentIndex == modelData.index
                badgeLabel: !!modelData.badgeLabel ? modelData.badgeLabel: ""

                DS3.MouseArea {
                    onClicked: {
                        if (currentIndex != modelData.index) {
                            currentIndex = modelData.index
                            currentIndexDiffer(modelData.index)
                        }
                    }
                }
            }

        }
    }
}

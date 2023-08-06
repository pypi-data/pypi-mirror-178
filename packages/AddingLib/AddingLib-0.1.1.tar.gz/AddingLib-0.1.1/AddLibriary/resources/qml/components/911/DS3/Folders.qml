import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3

// Athena 4.6

Rectangle {
// a model for the folder control
    default property alias model: listView.model
// current index to track which folder is selected
    property int currentIndex: 0

//  when current index changes this signal is emitted with the index that should become current
    signal currentIndexDiffer (int index)

    width: parent.width
    height: 40

    color: ui.ds3.bg.high

    ListView {
        id: listView

        anchors {
            fill: parent
            leftMargin: 16
        }

        orientation: ListView.Horizontal
        clip: true
        spacing: 16

        delegate: DS3.AtomFolder {
            labelText: modelData.text
            isSelected: currentIndex == modelData.index
            badgeLabel: modelData.badgeLabel || ""
            iconSource: modelData.iconSource

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

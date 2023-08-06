import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.ProgressBar {
    id: progressBarStatus

    property var statusTexts: []

    height: 4 + textsColumn.height + 10

    Column {
        id: textsColumn

        width: parent.width

        anchors {
            horizontalCenter: progressBarStatus.horizontalCenter
            bottom: progressBarStatus.bottom
        }

        Repeater {
            model: statusTexts

            DS3.Text {
                width: parent.width

                color: ui.ds3.figure.secondary
                style: ui.ds3.text.body.MRegular
                horizontalAlignment: Text.AlignHCenter
                text: modelData
            }
        }
    }
}

import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    property alias title: titleItem.text
    property var value: ""
    property bool copy: false

    height: Math.max(column.height, 52)
    width: parent.width

    Column {
        id: column

        width: parent.width

        spacing: 8

        DS3.Text {
            id: titleItem

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.nonessential
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.LRegular
            text: value
            visible: !copy
        }

        DS.CopyText {
            width: parent.width

            text: value
            size: 16
            line: 24
            color: ui.colors.base
            visible: copy
        }
    }
}
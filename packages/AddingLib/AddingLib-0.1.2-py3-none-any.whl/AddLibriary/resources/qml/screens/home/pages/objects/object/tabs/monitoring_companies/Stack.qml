import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Column {
    id: companyStack

    property alias titleText: sectionTitleItem.text
    property alias sectionText: sectionItem.text
    property bool hasElide: false

    width: parent.width

    spacing: 4

    DS3.Text {
        id: sectionTitleItem

        width: parent.width

        style: ui.ds3.text.body.SRegular
        color: ui.ds3.figure.secondary
        elide: hasElide ? Text.ElideRight : Text.ElideNone
    }

    DS3.Text {
        id: sectionItem

        width: parent.width

        style: ui.ds3.text.body.LRegular
        color: ui.ds3.figure.base
        wrapMode: Text.WrapAnywhere
    }
}
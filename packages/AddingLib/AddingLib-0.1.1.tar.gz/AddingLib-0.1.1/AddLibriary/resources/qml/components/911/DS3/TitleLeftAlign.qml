import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.TitleMaster {
    width: parent.width
    height: textItem.height + 8

    textItem {
        horizontalAlignment: Text.AlignLeft
        elide: Text.ElideRight
    }
    color: ui.ds3.figure.transparent
}

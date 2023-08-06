import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.Text {
    property alias textButtonMouseArea: textButtonMouseArea

    style: ui.ds3.text.body.MRegular
    color: ui.ds3.figure.interactive
    horizontalAlignment: Text.AlignRight
    opacity: enabled ? 1 : 0.3

    DS3.MouseArea { id: textButtonMouseArea }
}
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
//  If button is Off
    property bool isOff
//  Button name
    property var buttonName: "Switch1"

    atomTitle {
        title: buttonName
        subtitle: isOff ? tr.off : tr.on
    }

    leftIcon.source: "qrc:/resources/images/Athena/views_icons/LsButton-M.svg"
}
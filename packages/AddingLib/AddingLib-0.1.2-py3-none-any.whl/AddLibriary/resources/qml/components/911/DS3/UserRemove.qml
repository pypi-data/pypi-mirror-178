import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.MasterUser {
    //  Right icon clicked
    signal rightIconClicked

    color: ui.ds3.bg.highest

    atomTitle{
        anchors {
            right: removeIcon.left
            rightMargin: 16
        }
    }

    DS3.ButtonIcon {
        id: removeIcon

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/CrossCircle-M.svg"
        color: ui.ds3.figure.attention
        visible: enabled

        onClicked: rightIconClicked()
    }
}
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.MasterGroupM {
    id: groupSwitch

//  If checked
    property alias checked: groupToggle.checked
//  Callback on toggle action
    property var onToggle: () => {
        checked = !checked
    }

    textColumn.anchors.right: groupToggle.left
    color: ui.ds3.bg.highest

    DS3.Switch {
        id: groupToggle

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        checked: false
        opacity: enabled ? 1 : 0.3

        DS3.MouseArea {
            onClicked: onToggle()
        }
    }
}

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.MasterGroupM {
    id: groupSelectionMulti

//  If group is selected
    property bool selected: false
//  On group selecting
    property var onSelectedCallback: () => selected = !selected

    width: parent.width

    textColumn.anchors.right: mark.left
    color: ui.ds3.bg.highest

    DS3.Select {
        id: mark

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        size: DS3.Select.ComponentSize.S
        hasBackground: true
        checked: selected
        cancelBinding: false
    }

    DS3.MouseArea {
        onClicked: onSelectedCallback()
    }
}

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.MasterGroupM {
    id: groupSelectionMulti

//  If group is selected
    property bool selected: false
//  On group selecting
    property var onSelectedCallback: () => {
        selected = !selected
    }

    width: parent.width

    textColumn.anchors.right: selectMulti.left
    color: ui.ds3.bg.highest

    DS3.SelectMulti {
        id: selectMulti

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        checked: groupSelectionMulti.selected
        opacity: enabled ? 1 : 0.3
    }

    DS3.MouseArea {
        onClicked: {
            onSelectedCallback()
        }
    }
}

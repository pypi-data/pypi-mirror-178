import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.MasterGroupM {
    id: masterGroup

//  Link for group image
    property var imageSourceLink: ""
//  Title text
    property var groupTitle: ""
//  When clicked on settings gear icon
    property var settingsGearClicked: () => {}
//  When clicked on the element not in area of other icons
    property var groupRegularClicked: () => {}
//  Input variables
//  Group ID for right display
    property var groupID
//  Device count for right display
    property var deviceCount

    color: ui.ds3.bg.highest
    image {
        layer.enabled: image.status == Image.Ready
        source: imageSourceLink == "WRONG" ? "" : imageSourceLink
    }
    textColumn.anchors.right: settingsGear.left
    descText.text: !deviceCount ? tr.no_devices_lable : tr.devices_count_desktop + ": " + deviceCount
    status: deviceCount ? ui.ds3.status.DEFAULT : ui.ds3.status.WARNING
    atomTitle {
        titleItem.wrapMode: Text.Wrap
        title: groupTitle
        subtitle: groupID ? "ID " + groupID : ""
        elide: Text.ElideNone
    }

    DS3.MouseArea {
        onClicked: groupRegularClicked()
    }

    DS3.Icon {
        id: actionArrow

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/ActionArrow.svg"
        color: ui.ds3.figure.nonessential
        opacity: enabled ? 1 : 0.3
    }

    DS3.ButtonIcon {
        id: settingsGear

        anchors {
            right: actionArrow.left
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/Settings-M.svg"
        color: ui.ds3.figure.interactive
        opacity: enabled ? 1 : 0.3

        onClicked: settingsGearClicked()
    }
}

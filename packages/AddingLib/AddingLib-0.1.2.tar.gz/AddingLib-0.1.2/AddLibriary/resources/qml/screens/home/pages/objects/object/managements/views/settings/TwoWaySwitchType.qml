import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.InfoTitleButtonIcon {
    width: parent.width

    atomTitle.title: tr.two_way_switch_title
    leftIcon {
        source: "qrc:/resources/images/Athena/views_icons/LsPaired-M.svg"
        color: ui.ds3.figure.base
    }
    buttonIcon.source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"

    onRightControlClicked: Popups.popupByPath(
        "qrc:/resources/qml/components/911/DS3/popups/ModalInfo.qml",
        {
            sections: [{
                "description": tr.two_way_switch_descr
            }]
        }
    )
}
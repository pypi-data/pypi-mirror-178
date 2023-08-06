import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.InfoTitleButtonIcon {
    property bool isSensorBroken: device.is_any_sensor_broken

    visible: isSensorBroken || device.is_any_sensor_out_of_passport_range
    atomTitle.subtitle: isSensorBroken ? tr.faulty_sensor_lq_title : tr.malfunction
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Warning-M.svg"
    status: isSensorBroken ? ui.ds3.status.WARNING : ui.ds3.status.ATTENTION
    buttonIcon {
        source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"
        color: ui.ds3.figure.interactive
    }

    onRightControlClicked: {
        let sections = (isSensorBroken ? [{"description": tr.faulty_sensor_lq_descr}] :
            [{
                "title": tr.air_quality_out_range_title,
                "description": tr.air_quality_out_range_descr
            }])
        Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/ModalInfo.qml", {sections})
    }
}
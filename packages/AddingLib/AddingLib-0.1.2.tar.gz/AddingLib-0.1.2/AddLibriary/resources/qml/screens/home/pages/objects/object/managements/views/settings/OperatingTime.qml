import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
//  Which duration time to display
    property var duration_time: ""

    atomTitle {
        title: tr.shutoff_time_lightswitch
        subtitle: duration_time
    }

    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Timer-M.svg"
}
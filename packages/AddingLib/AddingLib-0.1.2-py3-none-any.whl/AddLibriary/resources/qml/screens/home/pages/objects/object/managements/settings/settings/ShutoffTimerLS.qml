import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    property var duration: [10, 30, 60, 300, 600, 900, 1800, 2700, 3600, 5400, 7200]
    property var time: null

    model: ["10 " + tr.sec, "30 " + tr.sec, "1 " + tr.min, "5 " + tr.min, "10 " + tr.min,
        "15 " + tr.min, "30 " + tr.min, "45 " + tr.min, "1 " + tr.hour,
        "1 " + tr.hour + " 30 " + tr.min, "2 " + tr.hours]

    currentIndex: duration.indexOf(time)
    atomTitle.title: tr.shutoff_time_lightswitch

    onActivated: {
        time = duration[index]
    }
}
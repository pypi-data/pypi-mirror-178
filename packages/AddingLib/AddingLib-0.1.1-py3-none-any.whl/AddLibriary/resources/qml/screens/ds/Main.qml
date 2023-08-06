import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml" as Root
import "qrc:/resources/js/images.js" as Images


Item {
    anchors.fill: parent

    DS3.Switch {
        id: enablingSwitch

        z: 1
        checked: true

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 30
        }

        onToggle: () => checked = !checked
    }

    DS3.ButtonIcon {
        id: backIcon

        anchors {
            top: parent.top
            topMargin: 12
            left: parent.left
            leftMargin: 12
        }

        z: 1

        source: "qrc:/resources/images/Athena/common_icons/Back-M.svg"

        onClicked: {
            screenLoader.source = "qrc:/resources/qml/screens/login/Login.qml"
        }
    }

    DS3.ScrollView {
        Column {
            anchors.horizontalCenter: parent.horizontalCenter

            width: parent.width / 3 - 20

            spacing: 40
            enabled: enablingSwitch.checked

            DS3.Text {
                style: ui.ds3.text.title.LBold
                text: "InputSearch"
            }

            DS3.InputSearch {
                id: searchField

                width: parent.width
                searchValue: ""
            }

            Block {
                title: "Agreement"

                DS3.Agreement {
                    text: tr.automatically_download_when_created

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }

                DS3.Agreement {
                    text: tr.i_have_read_and_agree + ": " + "<a style='text-decoration:none' href='https://www.google.com.ua/'>" + util.colorize(tr.a911_terms_of_use, ui.ds3.figure.interactive) + "</a>" + ", " + "<a style='text-decoration:none' href='https://www.google.com.ua/'>" + util.colorize(tr.a911_privacy_policy, ui.ds3.figure.interactive) + "</a>" + ", " + "<a style='text-decoration:none' href='https://www.google.com.ua/'>" + util.colorize(util.insert(tr.ajax_software_license_agreement, ["", "", ""]), ui.ds3.figure.interactive) + "</a>"

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }
            }

            Block {
                title: "AtomConnection"

                DS3.AtomConnection {
                   strength: 0
                }
                DS3.AtomConnection {
                   strength: 1
                }
                DS3.AtomConnection {
                   strength: 2
                }
                DS3.AtomConnection {
                   strength: 3
                }
            }
            Block {
                title: "AtomFolder 4.6"

                Row {
                    height: 40

                    spacing: 16
                    DS3.AtomFolder {
                        labelText: "Devices"
                        isSelected: true
                        badgeLabel: "2"
                        iconSource: "qrc:/resources/images/Athena/common_icons/Hub-S.svg"
                    }
                    DS3.AtomFolder {
                        labelText: "Rooms"
                        isSelected: false
                        iconSource: "qrc:/resources/images/Athena/common_icons/Rooms-S.svg"
                    }
                    DS3.AtomFolder {
                        labelText: "Notifications"
                        isSelected: false
                        iconSource: "qrc:/resources/images/Athena/common_icons/Notifications-S.svg"
                    }
                    DS3.AtomFolder {
                        labelText: "Control"
                        isSelected: false
                        iconSource: "qrc:/resources/images/Athena/common_icons/Control-S.svg"
                    }
                }
            }
            Block {
                title: "AtomInput"

                DS3.AtomInput {
                    width: parent.width

                    label: "AtomInput"
                }
            }

            Block {
                title: "AtomInputMultiLine"

                DS3.AtomInputMultiLine {
                    width: parent.width

                    label: "AtomInputMultiLine"
                }
            }

            Block {
                title: "AtomSliderColor"

                DS3.AtomSliderColor {
                    width: parent.width
                    model: [...Array(100).keys()]
                }
            }

            Block {
                title: "AtomSliderDual"

                DS3.AtomSliderDual {
                    id: dual

                    width: parent.width

                    model: [...Array(100).keys()]
                    firstValue: 25
                    secondValue: 75
                }
            }

            Block {
                title: "AtomTitle"

                DS3.AtomTitle {}
                DS3.AtomTitle {
                    isBold: true
                }
                DS3.AtomTitle {
                    isPrimary: false
                    isBold: true
                }
                DS3.AtomTitle {
                    isPrimary: false
                }
                DS3.AtomTitle {
                    subtitle: "Subtitle"
                }
                DS3.AtomTitle {
                    isBold: true
                    subtitle: "Subtitle"
                }
                DS3.AtomTitle {
                    isBold: true
                    title: "Title"
                    subtitle: "Subtitle"
                    badge: "Label"
                }
                DS3.AtomTitle {
                    isPrimary: false
                    subtitle: "Subtitle"
                }
                DS3.AtomTitle {
                    isPrimary: false
                    isBold: true
                    subtitle: "Subtitle"
                }
                DS3.AtomTitle {
                    isBold: true
                    badge: "Label"
                }
                DS3.AtomTitle {
                    title: "Title"
                    subtitle: "Subtitle"
                    subtitleColor: ui.ds3.figure.attention
                }
                DS3.AtomTitle {
                    title: "Title"
                    subtitle: "Subtitle"
                    subtitleIcon.source: "qrc:/resources/images/Athena/common_icons/Timer-S.svg"
                }
            }

            Block {
                title: "AtomSlider"

                DS3.AtomSlider {
                    width: parent.width
                    model: [1,2,3,4]
                }
            }

            Block {
                title: "BadgeLabel"

                DS3.BadgeLabel {
                    text: "BadgeLabel"
                    color: ui.ds3.figure.interactive
                }

                DS3.BadgeLabel {
                    text: "User"
                    isOutline: true
                }

                DS3.BadgeLabel {
                    text: "Admin"
                    isOutline: true
                    outlineColor: ui.ds3.figure.interactive
                }
            }


            Block {
                title: "BadgeAttention"

                DS3.BadgeAttention {
                    text: "4"
                }
                DS3.BadgeAttention {
                    text: "2"
                }
            }

            Block {
                title: "BadgeRegular 4.6"

                Row {
                    spacing: 16

                    DS3.BadgeRegular {
                        text: "1"
                    }
                    DS3.BadgeRegular {
                        text: "12"
                    }
                    DS3.BadgeRegular {
                        text: "123"
                    }
                }
            }

            Block {
                title: "BadgeStatusIconsText"

                DS3.BadgeStatusIconsText {
                    text: "123"
                }

                DS3.BadgeStatusIconsText {
                    icon: "qrc:/resources/images/Athena/common_icons/Humidity-S.svg"
                    text: "123"
                    status: ui.ds3.status.WARNING
                }

                DS3.BadgeStatusIconsText {
                    text: "123"

                    status: ui.ds3.status.HAZARD
                }
            }

            Block {
                title: "ButtonBar"

                DS3.ButtonBar {
                    buttonText: "ButtonBar"
                }

                DS3.ButtonBar {
                    buttonText: "ButtonBar"
                    hasBackground: true
                }

                DS3.ButtonBar {
                    buttonText: "ButtonBar"
                    hasComment: true
                    commentText: "Comment"
                    hasBackground: true
                }

                DS3.ButtonBar {
                    buttonText: "ButtonBar"
                    hasStepper: true
                    stepAmount: 12
                    currentStep: 7
                    hasBackground: true
                }

                DS3.ButtonBar {
                    buttonText: "ButtonBar"
                    hasComment: true
                    commentText: "Comment"
                    hasStepper: true
                    hasBackground: true
                }

                DS3.ButtonBar {
                    buttonText: "FirstButton"
                    hasBackground: true

                    buttons: DS3.ButtonText {
                        text: tr.cancel
                    }
                }

                DS3.ButtonBar {
                    buttonText: "ButtonBar"
                    hasComment: true
                    commentText: "Comment"
                    hasStepper: true
                    hasBackground: true

                    buttons: DS3.ButtonText {
                        text: tr.cancel
                    }
                }

                DS3.ButtonBar {
                    buttonText: "ButtonBar"
                    hasComment: true
                    commentText: "Comment"
                    hasStepper: true
                    hasBackground: true

                    buttons: [
                        DS3.ButtonContained {
                            text: "SecondButton"
                        },
                        DS3.ButtonContained {
                            text: tr.save
                        }
                    ]
                }
            }

            Block {
                title: "ButtonContained"

                DS3.ButtonContained {
                    width: parent.width

                    text: "Button parent width"
                }

                DS3.ButtonContained {
                    text: "Button with icon"
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                }

                DS3.ButtonContained {
                    text: "Button with icon"
                    isAttention: true
                }

                DS3.ButtonContained {
                    text: "Button with icon"
                    isAttention: true
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                }

                DS3.ButtonContained {
                    width: 300
                    text: "ButtonButtonButtonButtonButtonButton"
                }

                DS3.ButtonContained {
                    width: 300
                    text: "ButtonButtonButtonButtonButtonButton"
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                }

                DS3.ButtonContained {
                    text: "Button Loading"
                    isLoadState: true
                }

                DS3.ButtonContained {
                    width: parent.width

                    text: "Button Loading parent width"
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                    isLoadState: true
                }
            }

            Block {
                title: "ButtonIcon"

                DS3.ButtonIcon {
                    source: "qrc:/resources/images/Athena/common_icons/Settings-M.svg"
                }
            }

            Block {
                title: "ButtonMini"

                DS3.ButtonMini {
                    color: ui.ds3.figure.interactive
                    source: "qrc:/resources/images/Athena/common_icons/Impulse-M.svg"
                }
            }

            Block {
                title: "ButtonMiniDeviceSpread"

                DS3.ButtonMiniDeviceSpread {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                        subtitleIcon.source: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
                    }
                    buttonMini.source: "qrc:/resources/images/Athena/common_icons/Impulse-M.svg"
                }

                DS3.ButtonMiniDeviceSpread {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    buttonMini.source: "qrc:/resources/images/Athena/common_icons/Impulse-M.svg"
                }

                DS3.ButtonMiniDeviceSpread {
                    atomTitle {
                        title: "Title"
                    }
                    buttonMini.source: "qrc:/resources/images/Athena/common_icons/Impulse-M.svg"
                }
            }

            Block {
                title: "ButtonNavigation"

                DS3.ButtonNavigation {
                    icon: "qrc:/resources/images/Athena/common_icons/Forward-M.svg"

                    onClicked: console.log("button navigation clicked")
                }

                DS3.ButtonNavigation {
                    icon: "qrc:/resources/images/Athena/common_icons/ChevronLeft-M.svg"
                    text: "Button navigation"

                    onClicked: console.log("button navigation clicked")
                }
            }

            Block {
                title: "ButtonOutlined"

                DS3.ButtonOutlined {
                    width: parent.width

                    text: "Button parent width"
                }

                DS3.ButtonOutlined {
                    text: "Button with icon"
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                }

                DS3.ButtonOutlined {
                    text: "Button with icon"
                    isAttention: true
                }

                DS3.ButtonOutlined {
                    text: "Button with icon"
                    isAttention: true
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                }

                DS3.ButtonOutlined {
                    width: 300
                    text: "ButtonButtonButtonButtonButtonButton"
                }

                DS3.ButtonOutlined {
                    width: 300
                    text: "ButtonButtonButtonButtonButtonButton"
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                }

                DS3.ButtonOutlined {
                    text: "Button Loading"
                    isLoadState: true
                }

                DS3.ButtonOutlined {
                    width: parent.width

                    text: "Button Loading parent width"
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                    isLoadState: true
                }
            }

            Block {
                title: "ButtonRow"

                DS3.ButtonRow {
                    width: 100

                    text: "ButtonRow"
                }

                DS3.ButtonRow {
                    text: "ButtonRow"
                    isDanger: true
                }

                DS3.ButtonRow {
                    width: 40

                    text: "ButtonRow"
                    rowLeftAlign: true
                }

                DS3.ButtonRow {
                    width: 400

                    text: "ButtonRow"
                    rowLeftAlign: true
                }
            }

            Block {
                title: "ButtonText"

                DS3.ButtonText {
                    width: parent.width

                    text: "Button parent width"
                }

                DS3.ButtonText {
                    text: "Button with icon"
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                }

                DS3.ButtonText {
                    text: "Button with icon"
                    isAttention: true
                }

                DS3.ButtonText {
                    text: "Button with icon"
                    isAttention: true
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                }

                DS3.ButtonText {
                    width: 300
                    text: "ButtonButtonButtonButtonButtonButton"
                }

                DS3.ButtonText {
                    width: 300
                    text: "ButtonButtonButtonButtonButtonButton"
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                }

                DS3.ButtonText {
                    text: "Button Loading"
                    isLoadState: true
                }

                DS3.ButtonText {
                    width: parent.width

                    text: "Button Loading parent width"
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Plus-S.svg"
                    isLoadState: true
                }
            }

            Block {
                title: "CarrouselContainerStack"

                DS3.CarrouselContainerStack {
                    width: parent.width

                    devicesModel: ["CARD", "TAG", "01", "02", "03"]
                    colorPeaker.colorModel: [
                        {
                            text: tr.black,
                            circleColor: ui.ds3.special.black,
                            serverColor: "BLACK",
                        },
                        {
                            text: tr.white,
                            circleColor: ui.ds3.special.white,
                            serverColor: "WHITE",
                        },
                        {
                            text: tr.black,
                            circleColor: ui.ds3.special.black,
                            serverColor: "BLACK",
                        },
                        {
                            text: tr.white,
                            circleColor: ui.ds3.special.white,
                            serverColor: "WHITE",
                        },
                    ]
                }
            }

            Block {
                title: "ChangesChecker"

                DS3.ChangesChecker {
                    id: changesChecker

                    listeningValues: [
                        autoSaverInput.atomInput.text,
                        autoSaverCompanySelection.checked,
                        autoSaverDatePicker.checkedDays
                    ]
                }

                DS3.InputSingleLine {
                    id: autoSaverInput
                }

                DS3.CompanySelection {
                    id: autoSaverCompanySelection
                }

                DS3.DatePicker {
                    id: autoSaverDatePicker

                    onCheckedDaysChanged: console.log(JSON.stringify(checkedDays))
                }

                DS3.ButtonContained {
                    text: "Save changes"

                    enabled: changesChecker.hasChanges

                    onClicked: {
                        changesChecker.changeInitialValues()
                    }
                }
            }

            Block {
                title: "CheckBoxRound"

                DS3.CheckBoxRound {
                    text: "123"

                    onClicked: {
                        isOutline = !isOutline
                    }
                }

                DS3.CheckBoxRound {
                    text: "456"

                    onClicked: {
                        isOutline = !isOutline
                    }
                }
            }

            Block {
                title: "ChipColor"

                DS3.ChipColor {
                    circleColor: ui.ds3.special.black
                    mainText: "Black"
                    isSelected: true
                }
                DS3.ChipColor {
                    circleColor: ui.ds3.special.white
                    mainText: "White"
                }
            }

            Block {
                title: "ChipControlColor"

                DS3.ChipControlColor {
                    colorModel: [
                        {
                            text: tr.black,
                            circleColor: ui.ds3.special.black,
                            serverColor: "BLACK",
                        },
                        {
                            text: "Knob",
                            circleColor: ui.ds3.special.knob,
                            serverColor: "KNOB",
                        },
                        {
                            text: "Hole",
                            circleColor: ui.ds3.special.hole,
                            serverColor: "HOLE",
                        },
                        {
                            text: tr.white,
                            circleColor: ui.ds3.special.white,
                            serverColor: "WHITE",
                        },
                    ]
                }
            }

            Block {
                title: "CompanyImage"

                DS3.CompanyImage {
                    source: ""
                    name: "Company A"
                }

                DS3.CompanyImage {
                    width: 64
                    height: 64

                    source: "https://ajax-cdn-stage.s3.eu-west-3.amazonaws.com/imagesvc/public/app_a911/image_5ff5851d54cfce61173350bf/64x64/download.jpeg"
                    name: "Company A"
                }
            }

            Block {
                title: "CompanyImageUpload"
                DS3.CompanyImageUpload {
                    property var appCompany: null
                    imageRect.source: "https://ajax-cdn-stage.s3.eu-west-3.amazonaws.com/imagesvc/public/app_a911/image_5ff5851d54cfce61173350bf/64x64/download.jpeg"
                }
            }
            Block {
                title: "Comment"

                DS3.Comment {
                    text: "Ready for test"
                }

                DS3.Comment {
                    text: "Power supply is interrupted due to short circuit"
                    itemsColor: ui.ds3.figure.attention
                }

                DS3.Comment {
                    text: "Ready for test"
                    icon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
                }

                DS3.Comment {
                    text: "Power supply is interrupted due to short circuit"
                    icon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
                    itemsColor: ui.ds3.figure.attention
                }
            }

            Block {
                title: "CommentImportant"

                DS3.CommentImportant {
                    atomTitle.title: "Title"
                    atomTitle.subtitle: "Subtitle"
                }

                DS3.CommentImportant {
                    atomTitle.title: "Title"
                }

                DS3.CommentImportant {
                    atomTitle.title: "Title"
                    atomTitle.subtitle: "Subtitle"
                    status: DS3.CommentImportant.Status.Attention
                }

                DS3.CommentImportant {
                    atomTitle.title: "Title"
                    status: DS3.CommentImportant.Status.Attention
                }

                DS3.CommentImportant {
                    atomTitle.title: "Title"
                    atomTitle.subtitle: "Subtitle"
                    status: DS3.CommentImportant.Status.Warning
                }

                DS3.CommentImportant {
                    atomTitle.title: "Title"
                    status: DS3.CommentImportant.Status.Warning
                }


                DS3.CommentImportant {
                    atomTitle.title: "Title"
                    atomTitle.subtitle: "Subtitle"
                    imageItem.visible: false
                }

                DS3.CommentImportant {
                    atomTitle.title: "Title"
                    imageItem.visible: false
                }
            }

            Block {
                title: "CommentPasscode"

                DS3.CommentPasscode {
                    atomTitle.title: "Title"
                }

                DS3.CommentPasscode {
                    atomTitle.title: "Title"
                    firstSubtitle.text: "Subtitle"
                    secondSubtitle.text: "Subtitle"
                    thirdSubtitle.text: "Subtitle"
                    firstIcon {
                        source: "qrc:/resources/images/Athena/views_icons/Photo-S.svg"
                        color: ui.ds3.figure.base
                    }
                    secondIcon {
                        source: "qrc:/resources/images/Athena/views_icons/Photo-S.svg"
                        color: ui.ds3.figure.base
                    }
                }
            }

            Block {
                title: "CompanyNavigation"

                DS3.CompanyNavigation {
                    companyName.text: "First Very Long Company Name The Second"

                    onRightIconClicked: {
                        console.log("First Company clicked")
                    }
                }

                DS3.CompanyNavigation {
                    companyName.text: "Second Company"
                    companyImage.source: "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png"

                    onRightIconClicked: {
                        console.log("Second Company clicked")
                    }
                }
            }

            Block {
                title: "CompanySelection"

                DS3.CompanySelection {
                    companyName.text: "First Very Long Company Name The Second"

                    companyChecked: () => {
                        checked = !checked
                    }
                }

                DS3.CompanySelection {
                    companyName.text: "Second Company"
                    companyImage.source: "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png"

                    companyChecked: () => {
                        checked = !checked
                    }
                }
            }

            Block {
                title: "CompanySelectionSingle"

                DS3.CompanySelection {
                    companyName.text: "Company Selection"
                }
            }

            Block {
                title: "ConnectionStatusRow"

                DS3.ConnectionStatusRow {}

                DS3.ConnectionStatusRow {
                    firstIconStatus: DS3.ConnectionStatusRow.IconStatus.Fail
                    secondIconStatus: DS3.ConnectionStatusRow.IconStatus.Loading
                }
            }

            Block {
                title: "DatePicker"

                width: 450

                DS3.DatePicker {}
            }

            Block {
                title: "DeviceButtonIcon"

                DS3.DeviceButtonIcon {
                    width: parent.width

                    buttonIconSource: "qrc:/resources/images/Athena/views_icons/Info-M.svg"
                    deviceType: "25"
                    deviceColor: "WHITE"
                    atomTitle {
                        title: "Camera"
                        subtitle: "random text"
                    }
                    onRightControlClicked: () => {console.log("----DeviceButtonIcon--clicked--->")}
                }

                DS3.DeviceButtonIcon {
                    width: parent.width

                    buttonIconSource: "qrc:/resources/images/Athena/views_icons/Info-M.svg"
                    deviceType: "25"
                    deviceColor: "WHITE"
                    atomTitle {
                        title: "Camera"
                        subtitle: "random text"
                    }
                    badgeCounter: 1

                    onRightControlClicked: () => {
                        console.log("----DeviceButtonIcon--clicked--->")
                        badgeCounter += 1
                    }
                }

                DS3.DeviceButtonIcon {
                    width: parent.width

                    buttonIconSource: "qrc:/resources/images/Athena/views_icons/Info-M.svg"
                    deviceType: "25"
                    deviceColor: "WHITE"
                    atomTitle {
                        title: "Camera"
                        subtitle: "random text"
                    }
                    isOnline: false

                    onRightControlClicked: () => {console.log("----DeviceButtonIcon--clicked--->")}
                }

            }

            Block {
                title: "DeviceButtonMini"

                DS3.DeviceButtonMini {
                    width: parent.width

                    deviceType: "25"
                    deviceColor: "WHITE"
                    atomTitle {
                        title: "Camera"
                        subtitle: "random text"
                    }
                    buttonMiniSource: "qrc:/resources/images/Athena/views_icons/Photo-S.svg"

                    onRightControlClicked: () => {console.log("----DeviceButtonMini--clicked--1--->")}
                }

                DS3.DeviceButtonMini {
                    id: deviceButtonMini

                    width: parent.width

                    deviceType: "25"
                    deviceColor: "WHITE"
                    atomTitle {
                        title: "Camera"
                        subtitle: "random text"
                    }
                    buttonMiniSource: "qrc:/resources/images/Athena/views_icons/Photo-S.svg"

                    onRightControlClicked: () => {
                        hasSpinner = true
                        enabled = false
                        deviceButtonMiniSpinnerTimer.start()
                     }

                     Timer {
                        id: deviceButtonMiniSpinnerTimer

                        interval: 1500 // milliseconds
                        repeat: false

                        onTriggered: {
                            deviceButtonMini.hasSpinner = false
                            deviceButtonMini.enabled = true
                        }
                    }
                }
            }

            Block {
                title: "DeviceCardNavigation"

                DS3.DeviceCardNavigation {
                    width: 300

                    imageSource: Images.get_image("fibra_hub", "Medium", "BLACK")
                    atomTitle {
                        title: "Hub Fibra"
                        subtitle: "ID 00000001"
                    }
                    isOnline: true
                }

                DS3.DeviceCardNavigation {
                    width: 300

                    imageSource: Images.get_image("21", "Medium", "BLACK")
                    atomTitle {
                        title: "Hub Online Loooooooooooooooooooong"
                        subtitle: "ID 00000002"
                    }
                    isOnline: true
                }

                DS3.DeviceCardNavigation {
                    width: 300

                    imageSource: Images.get_image("21", "Medium", "WHITE")
                    statusText: tr.offline
                    badgeCounter: "3"
                    atomTitle {
                        title: "Hub offline"
                        subtitle: "ID 00000003"
                    }
                    isOnline: false
                }
            }

            Block {
                title: "DeviceTwoLinesSelectionMulti"

                DS3.DeviceTwoLinesSelectionMulti {
                    width: parent.width

                    deviceType: "44"
                    deviceColor: "WHITE"
                    deviceSubtype: "LIGHT_SWITCH_TWO_GANG"
                    firstButtonName: "Left Button Name"
                    secondButtonName: "Right Button Name"
                    atomTitle {
                        title: "Light Switch Two Gang"
                        subtitle: "Test Room"
                    }

                    firstButtonClickedArea.onClicked: {
                        firstButtonChecked = !firstButtonChecked
                    }

                    secondButtonClickedArea.onClicked: {
                        secondButtonChecked = !secondButtonChecked
                    }
                }

                DS3.DeviceTwoLinesSelectionMulti {
                    width: parent.width

                    deviceType: "44"
                    deviceColor: "WHITE"
                    deviceSubtype: "LIGHT_SWITCH_TWO_GANG"
                    firstButtonName: "Left Button Name Button Name Button Name Button Name Button Name Button Name Button Name Button Name Button Name"
                    secondButtonName: "Right Button Name Button Name Button Name Button Name Button Name Button Name Button Name Button Name Button Name"
                    atomTitle {
                        title: "Light Switch Two Gang"
                        subtitle: "Test Room"
                    }
                    description.text: "Room Room Room Room Room Room Room Room Room Room Room Room Room Room Room Room Room Room Room"

                    firstButtonClickedArea.onClicked: {
                        firstButtonChecked = !firstButtonChecked
                    }

                    secondButtonClickedArea.onClicked: {
                        secondButtonChecked = !secondButtonChecked
                    }
                }
            }

            Block {
                title: "DeviceNavigation"

                DS3.DeviceNavigation {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Ok"
                    badgeCounter: "1"
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }

                DS3.DeviceNavigation {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "A simple yet elegant device capable of protecting the whole family"
                    atomTitle.subtitle: "DoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtect"
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }

                DS3.DeviceNavigation {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Ok"
                    isOnline: false
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }
            }

            Block {
                title: "DeviceNavigationSmall"

                DS3.DeviceNavigationSmall {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Ok"

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                    }
                }

                DS3.DeviceNavigationSmall {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                    }
                }

                DS3.DeviceNavigationSmall {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Room Room Room Room Room Room Room Room Room Room Room"

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                    }
                }
            }

            Block {
                title: "DeviceNavigationButtonMini"

                DS3.DeviceNavigationButtonMini {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle {
                        title: "Door Protect"
                        subtitle: "Ok"
                    }
                    badgeCounter: "1"
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]
                    buttonMiniDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                            subtitleIcon.source: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
                        }
                        buttonMini {
                            source: "qrc:/resources/images/Athena/common_icons/Impulse-M.svg"

                            onClicked: {
                                console.log("ButtonMini clicked")
                            }
                        }
                    }

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                        console.log("Main area clicked")
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }

                DS3.DeviceNavigationButtonMini {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle {
                        title: "A simple yet elegant device capable of protecting the whole family"
                        subtitle: "DoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtect"
                    }
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]
                    buttonMiniDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                            subtitleIcon.source: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
                        }
                        buttonMini {
                            source: "qrc:/resources/images/Athena/common_icons/Impulse-M.svg"

                            onClicked: {
                                console.log("ButtonMini clicked")
                            }
                        }
                    }

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                        console.log("Main area clicked")
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }

                DS3.DeviceNavigationButtonMini {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle {
                        title: "A simple yet elegant device capable of protecting the whole family"
                        subtitle: "DoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtect"
                    }
                    isOnline: false

                    buttonMiniDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                            subtitleIcon.source: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
                        }
                        buttonMini {
                            source: "qrc:/resources/images/Athena/common_icons/Impulse-M.svg"

                            onClicked: {
                                console.log("ButtonMini clicked")
                            }
                        }
                    }

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                        console.log("Main area clicked")
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }
            }

            Block {
                title: "DeviceNavigationSwitch"

                DS3.DeviceNavigationSwitch {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle {
                        title: "Door Protect"
                        subtitle: "Ok"
                    }
                    badgeCounter: "1"
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]
                    switchDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                        }
                        onSwitched: () => switchDeviceSpread.switchChecked = !switchDeviceSpread.switchChecked
                        switchControl.cancelBinding: false
                    }

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                        console.log("Main area clicked")
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }

                DS3.DeviceNavigationSwitch {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle {
                        title: "A simple yet elegant device capable of protecting the whole family"
                        subtitle: "DoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtect"
                    }
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]
                    switchDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                        }
                        onSwitched: () => switchDeviceSpread.switchChecked = !switchDeviceSpread.switchChecked
                        switchControl.cancelBinding: false
                    }

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                        console.log("Main area clicked")
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }

                DS3.DeviceNavigationSwitch {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle {
                        title: "A simple yet elegant device capable of protecting the whole family"
                        subtitle: "DoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtect"
                    }
                    isOnline: false

                    switchDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                        }
                        onSwitched: () => switchDeviceSpread.switchChecked = !switchDeviceSpread.switchChecked
                        switchControl.cancelBinding: false
                    }

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                        console.log("Main area clicked")
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }
            }

            Block {
                title: "DeviceTwoLinesNavigationSwitch"

                DS3.DeviceTwoLinesNavigationSwitch {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle {
                        title: "A simple yet elegant device capable of protecting the whole family"
                        subtitle: "DoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtectDoorProtect"
                    }
                    badgeCounter: "1"
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]
                    firstSwitchDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                        }
                        onSwitched: () => firstSwitchDeviceSpread.switchChecked = !firstSwitchDeviceSpread.switchChecked
                        switchControl.cancelBinding: false
                    }
                    secondSwitchDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                        }
                        onSwitched: () => secondSwitchDeviceSpread.switchChecked = !secondSwitchDeviceSpread.switchChecked
                        switchControl.cancelBinding: false
                    }

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                        console.log("Main area clicked")
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }

                DS3.DeviceTwoLinesNavigationSwitch {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle {
                        title: "Door Protect"
                        subtitle: "Ok"
                    }
                    badgeCounter: "1"
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]
                    firstSwitchDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                        }
                        onSwitched: () => firstSwitchDeviceSpread.switchChecked = !firstSwitchDeviceSpread.switchChecked
                        switchControl.cancelBinding: false
                    }
                    secondSwitchDeviceSpread {
                        atomTitle {
                            title: "Title"
                            subtitle: "Subtitle"
                        }
                        onSwitched: () => secondSwitchDeviceSpread.switchChecked = !secondSwitchDeviceSpread.switchChecked
                        switchControl.cancelBinding: false
                    }

                    onActionArrowControlClicked: {
                        if (!isChosen) isChosen = true
                        console.log("Main area clicked")
                    }
                    onGearControlClicked: { console.log("Settings Gear") }
                }
            }

            Block {
                title: "DeviceOneLineSelectionMulti"

                DS3.DeviceOneLineSelectionMulti {
                    width: parent.width

                    deviceType: "44"
                    deviceColor: "BLACK"
                    deviceSubtype: "LIGHT_SWITCH_ONE_GANG"
                    buttonName: "Button Name"
                    atomTitle.title: "Light Switch One Gang"
                    atomTitle.subtitle: "Test Room 2"

                    buttonClickArea.onClicked: {
                        buttonChecked = !buttonChecked
                    }
                }

                DS3.DeviceOneLineSelectionMulti {
                    width: parent.width

                    deviceType: "44"
                    deviceColor: "BLACK"
                    deviceSubtype: "LIGHT_SWITCH_ONE_GANG"
                    buttonName: "Button Name Button Name Button Name Button Name Button Name Button Name Button Name"
                    atomTitle {
                        title: "Light Switch One Gang"
                        subtitle: "Test Room 2"
                    }
                    description.text: "LIGHT_SWITCH_ONE_GANG_LOOOOOOOOOOOOOOOOOOOOOOOONG DESCRIPTION"

                    buttonClickArea.onClicked: {
                        buttonChecked = !buttonChecked
                    }
                }
            }

            Block {
                title: "DeviceRegular"

                DS3.DeviceRegular {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Ok"
                    atomTitle.subtitleColor: ui.ds3.figure.positiveContrast
                }

                DS3.DeviceRegular {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Need more power"
                    atomTitle.subtitleColor: ui.ds3.figure.warningContrast
                }

                DS3.DeviceRegular {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "No power"
                    atomTitle.subtitleColor: ui.ds3.figure.attention
                }

                DS3.DeviceRegular {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "WHITE"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "No honey"
                    operator: DS3.DeviceRegular.OperatorType.Switch
                    switchChecked: true

                    onRightControlClicked: {
                        switchChecked = !switchChecked
                    }
                }

                DS3.DeviceRegular {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "No power"
                    flowIcoModel: [{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/SignalStrength3-S.svg"},{"color":"interactive","source":"qrc:/resources/images/Athena/status_icons/Battery100-S.svg"},{"color":"warningContrast","source":"qrc:/resources/images/Athena/status_icons/Warning-S.svg"}]
                    operator: DS3.DeviceRegular.OperatorType.NavigationArrow
                }

                DS3.DeviceRegular {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "No power"
                    operator: DS3.DeviceRegular.OperatorType.NavigationClue
                    actionArrowNumber: 123
                }

                DS3.DeviceRegular {
                    width: parent.width

                    imageSource: "qrc:/resources/images/Athena/migration/DeviceImage.svg"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "No power"
                    smallImage: true
                    operator: DS3.DeviceRegular.OperatorType.NavigationClue
                    actionArrowNumber: 123
                }

            }

            Block {
                title: "DeviceSimple"

                DS3.DeviceSimple {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Ok"
                }
            }

            Block {
                title: "DeviceSelectionSingle"

                DS3.DeviceSelectionSingle {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Ok"
                    checked: true

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }

                DS3.DeviceSelectionSingle {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "DoorProtect DoorProtect DoorProtect DoorProtect DoorProtect"
                    atomTitle.subtitle: "Room Room Room Room Room Room Room Room Room Room Room"
                    checked: true

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }
            }

            Block {
                title: "DeviceSelectionMulti"

                DS3.DeviceSelectionMulti {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Ok"
                    checked: true

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }

                DS3.DeviceSelectionMulti {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "Door Protect"
                    atomTitle.subtitle: "Ok"
                    checked: true
                    description.text: "Description"

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }

                DS3.DeviceSelectionMulti {
                    width: parent.width

                    deviceType: "01"
                    deviceColor: "BLACK"
                    atomTitle.title: "DoorProtect DoorProtect DoorProtect DoorProtect DoorProtect"
                    atomTitle.subtitle: "Room Room Room Room Room Room Room Room Room Room Room"
                    checked: true

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }
            }

            Block {
                title: "DownloadProgress"

                DS3.DownloadProgress {
                    atomTitle {
                        title: "Report #ХХХ ХХХ ХХХ"
                        subtitle: "01.12.21"
                    }
                }
            }

            Block {
                title: "Folder"

                DS3.Folder {
                    labelText: "Devices"
                    selected: true
                }
                DS3.Folder {
                    labelText: "Users"
                    selected: false
                }
                DS3.Folder {
                    labelText: "Hubs"
                    badgeLabel: "1"
                    selected: false
                }
                DS3.Folder {
                    labelText: "Private"
                    badgeLabel: "24"
                    selected: true
                }
            }

            Block {
                title: "FolderControl"

                DS3.FolderControl {
                    id: folderControl

                    onCurrentIndexDiffer: {
                        folderControl.currentIndex = index
                    }

                    enabled: enablingSwitch.checked
                    model:  [
                        { text: "Devices", index: 0 },
                        { text: "Users", index: 1 },
                        { text: "Hubs", index: 3, badgeLabel: "1" },
                        { text: "Private", index: 4, badgeLabel: "24" }
                    ]
                }
            }

            Block {
                title: "Folders 4.6"

                Column {
                    width: parent.width

                    spacing: 40

                    DS3.Folders {
                        id: folders

                        enabled: enablingSwitch.checked
                        model: [
                            {text: "Devices", index: 0, iconSource: "qrc:/resources/images/Athena/common_icons/Hub-S.svg"},
                            {text: "Users", index: 1, iconSource: "qrc:/resources/images/Athena/common_icons/Rooms-S.svg"},
                            {text: "Hubs", index: 3, badgeLabel: "1", iconSource: "qrc:/resources/images/Athena/common_icons/Notifications-S.svg"},
                            {text: "Private", index: 4, badgeLabel: "24", iconSource: "qrc:/resources/images/Athena/common_icons/Control-S.svg" }
                        ]
                    }

                    DS3.Folders {
                        id: folders2

                        enabled: enablingSwitch.checked
                        model: [
                            {text: "All", index: 0},
                            {text: "Security", index: 1},
                            {text: "Autmation", index: 3, badgeLabel: "2"}
                        ]
                    }
                    DS3.Folders {
                        id: folders3

                        enabled: enablingSwitch.checked
                        model: [
                            {text: "Devices", index: 0, iconSource: "qrc:/resources/images/Athena/common_icons/Hub-S.svg"},
                            {text: "Users", index: 1, iconSource: "qrc:/resources/images/Athena/common_icons/Rooms-S.svg"},
                            {text: "Hubs", index: 3, badgeLabel: "1", iconSource: "qrc:/resources/images/Athena/common_icons/Notifications-S.svg"},
                            {text: "Private", index: 4, badgeLabel: "24", iconSource: "qrc:/resources/images/Athena/common_icons/Control-S.svg" },
                            {text: "Devices", index: 0, iconSource: "qrc:/resources/images/Athena/common_icons/Hub-S.svg"},
                            {text: "Users", index: 1, iconSource: "qrc:/resources/images/Athena/common_icons/Rooms-S.svg"},
                            {text: "Hubs", index: 3, badgeLabel: "1", iconSource: "qrc:/resources/images/Athena/common_icons/Notifications-S.svg"},
                            {text: "Private", index: 4, badgeLabel: "24", iconSource: "qrc:/resources/images/Athena/common_icons/Control-S.svg" }
                        ]
                    }
                }
            }

            Block {
                title: "GroupImage"

                DS3.GroupImage {
                }

                DS3.GroupImage {
                    imageRect.source: "qrc:/resources/images/Athena/groups/Groups-Example-Image-Yard.png"
                }
            }

            Block {
                title: "GroupMultiSelection"

                DS3.GroupMultiSelection {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    descText.text: "Description"
                    selected: true

                    onSelectedCallback: () => {
                        console.log("GroupMultiSelection clicked.")
                        selected = !selected
                    }
                }

                DS3.GroupMultiSelection {
                    atomTitle.title: "Title"
                    selected: true

                    onSelectedCallback: () => {
                        console.log("GroupMultiSelection clicked.")
                        selected = !selected
                    }
                }

                DS3.GroupMultiSelection {
                    atomTitle.title: "Внутренний дворик нашего соседа слева от главного входа возле клумбы"
                    selected: true

                    onSelectedCallback: () => {
                        console.log("GroupMultiSelection clicked.")
                        selected = !selected
                    }
                }
            }

            Block {
                title: "GroupSingleSelection"

                DS3.GroupSingleSelection {
                    atomTitle.title: "Title"
                    selected: true

                    onSelectedCallback: () => {
                        console.log("GroupSingleSelection clicked")
                        selected = !selected
                    }
                }

                DS3.GroupSingleSelection {
                    atomTitle.title: "Title Title Title Title Title Title Title Title Title Title Title Title Title Title Title Title"
                    selected: false

                    onSelectedCallback: () => {
                        console.log("GroupSingleSelection clicked")
                        selected = !selected
                    }
                }
            }

            Block {
                title: "GroupSwitch"

                DS3.GroupSwitch {
                    atomTitle.title: "Title"
                    atomTitle.subtitle: "Subtitle"
                    descText.text: "Description"
                    checked: true
                }
            }

            Block {
                title: "Icon"

                DS3.Icon {
                    source: "qrc:/resources/images/Athena/common_icons/Back-M.svg"
                }

                DS3.Icon {
                    source: "qrc:/resources/images/Athena/status_icons/AlwaysActive-S.svg"
                    color: ui.ds3.figure.interactive
                }

                DS3.Icon {
                    source: "qrc:/resources/images/Athena/common_icons/Settings-M.svg"
                    color: ui.ds3.figure.interactive
                }
            }

            Block {
                title: "InfoContainerIcon"

                DS3.InfoContainerIcon {
                    icon.source: "qrc:/resources/images/Athena/common_icons/Settings-M.svg"
                    textElement.text: "Device ID can be found on the back side of the casing, near QR code"
                }
            }



            Block {
                title: "InfoFooter"

                DS3.Text {
                    text: "footerType: Device"
                }

                DS3.InfoFooter {
                    footerType: DS3.InfoFooter.FooterType.Device
                    title.text: "Ajax CombiProtect"
                    subtitleUpper.text: "Firmware v2.9.79"
                    subtitleLower.text: "Device ID 00084F78"
                }

                DS3.Text {
                    text: "footerType: User"
                }

                DS3.InfoFooter {
                    footerType: DS3.InfoFooter.FooterType.User
                    subtitleUpper.text: "User ID 502"
                }
            }

            Block {
                title: "InfoImage"

                DS3.InfoImage {
                    atomTitle.title: "I am non-random, concise text"
                    companyImage.source: "qrc:/resources/images/desktop/delegates/MotionCam/MotionCamWhiteMedium.png"
                }

                DS3.InfoImage {
                    atomTitle.title: "I am fake-random, non-concise and hell long text. Worst about me is the fact that I am not about something worthfull to read about. Shame on you if you still reading it. Gods of Time looks at you with a contempt and disgust. "
                    companyImage.source: "qrc:/resources/images/desktop/delegates/MotionCam/MotionCamWhiteMedium.png"
                }
            }

            Block {
                title: "InfoSession"

                DS3.InfoSession {
                    sessionVersion: "Ajax 2.22"
                    sessionDevice: "iPhone X, iOS 13.5.1"
                    sessionIp: "194.183.181.44"
                    sessionDate: "2022.01.07"
                    sessionTime: "10:24"
                }

                DS3.InfoSession {
                    sessionVersion: "Ajax 2.22"
                    sessionDevice: "iPhone X, iOS 13.5.1"
                }

                DS3.InfoSession {
                    sessionVersion: "Ajax 2.22"
                    sessionDevice: "iPhone X, iOS 13.5.1"
                    sessionIp: "194.183.181.44"
                    isCurrentSession: true
                }
            }

            Block {
                title: "InfoTitle"

                DS3.InfoTitle {
                    atomTitle.title: "Title"
                }

                DS3.InfoTitle {
                    atomTitle.title: "Title"
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                }

                DS3.InfoTitle {
                    atomTitle.title: "Title"
                    stateEnabled: false
                }

                DS3.InfoTitle {
                    atomTitle.title: "Title"
                    stateEnabled: false
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    stateEnabled: false
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    status: ui.ds3.status.WARNING
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.WARNING
                }


                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    status: ui.ds3.status.ATTENTION
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.ATTENTION
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    status: ui.ds3.status.HAZARD
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.HAZARD
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.WARNING
                    stateEnabled: false
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.ATTENTION
                    stateEnabled: false
                }

                DS3.InfoTitle {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.HAZARD
                    stateEnabled: false
                }
            }

            Block {
                title: "InfoTitleButtonIcon"

                DS3.Text {
                    text: "TitlePrimary"
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: "Title"

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>0")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: "Title"
                    status: ui.ds3.status.WARNING

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>0Warning")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: "Title"
                    status: ui.ds3.status.ATTENTION

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>0Attention")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: "Title"
                    status: ui.ds3.status.HAZARD

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>0Hazard")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: "Title"
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>1")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: "Title"
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.WARNING

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>1Warning")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: "Title"
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.ATTENTION

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>1Attention")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle.title: "Title"
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.HAZARD

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>1Hazard")}
                }

                DS3.Text {
                    text: "TitleSecondary"
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>2")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle {
                        title: "LONG_WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
                        subtitle: "Subtitle_LONG_WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
                    }

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>3")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    stateEnabled: false

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>4")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    stateEnabled: false
                    stateBehavoir: DS3.InfoTitleButtonIcon.StateBehavior.AlwaysEnabled

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>5")}
                }

                DS3.InfoTitleButtonIcon {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    stateBehavoir: DS3.InfoTitleButtonIcon.StateBehavior.AlwaysDisabled

                    onRightControlClicked: {console.log("Click!>>ButtonIcon>>6")}
                }
            }

            Block {
                title: "InfoTitleButtonMini"

                DS3.Text {
                    text: "TitlePrimary"
                }

                DS3.InfoTitleButtonMini {
                    atomTitle.title: "Title"

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>0")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle.title: "Title"
                    status: ui.ds3.status.ATTENTION

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>0")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle.title: "Title"
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>1")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle.title: "Title"
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                    status: ui.ds3.status.ATTENTION

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>0")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle.title: "Title"
                    stateEnabled: false

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>2")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle.title: "Title"
                    stateEnabled: false
                    stateBehavoir: DS3.InfoTitleButtonMini.StateBehavior.AlwaysEnabled

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>3")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle.title: "Title"
                    stateBehavoir: DS3.InfoTitleButtonMini.StateBehavior.AlwaysDisabled

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>4")}
                }

                DS3.Text {
                    text: "TitleSecondary"
                }

                DS3.InfoTitleButtonMini {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>5")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    status: ui.ds3.status.ATTENTION

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>5")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle {
                        title: "LONG_WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
                        subtitle: "Subtitle_LONG_WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
                    }

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>6")}
                }

                DS3.Text {
                    text: "operator: ButtonMini, stateEnabled: false"
                    color: ui.ds3.figure.secondary
                }

                DS3.InfoTitleButtonMini {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    stateEnabled: false

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>7")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    stateEnabled: false
                    stateBehavoir: DS3.InfoTitleButtonMini.StateBehavior.AlwaysEnabled

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>8")}
                }

                DS3.InfoTitleButtonMini {
                    atomTitle {
                        title: "Title"
                        subtitle: "Subtitle"
                    }
                    stateBehavoir: DS3.InfoTitleButtonMini.StateBehavior.AlwaysDisabled

                    onRightControlClicked: {console.log("Click!>>ButtonMini>>9")}
                }
            }

            Block {
                title: "InfoSignal"

                DS3.InfoSignal {
                    atomTitle.title: "Title"
                    atomConnection.strength: 0
                }

                DS3.InfoSignal {
                    atomTitle.title: "Title"
                    atomConnection.strength: 1
                }

                DS3.InfoSignal {
                    atomTitle.title: "Title"
                    atomConnection.strength: 2
                }

                DS3.InfoSignal {
                    atomTitle.title: "Title"
                    atomConnection.strength: 3
                }

                DS3.InfoSignal {
                    atomTitle.title: "Title"
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"
                    atomConnection.strength: 2
                }
            }

            Block {
                title: "InfoStatus"

                DS3.InfoStatus {
                    atomTitle.title: "Title"
                    atomTitle.subtitle: "Subtitle"
                }

                DS3.InfoStatus {
                    atomTitle.title: "Door"
                    atomTitle.subtitle: "In progress..."
                    atomTitle.subtitleColor: ui.ds3.figure.positiveContrast
                    source: Images.get_image("4c", "Small", "BLACK", null, "TYPE_G")
                }
            }

            Block {
                title: "Image"

                DS3.Image {
                    width: 72
                    height: 72

                    source: "qrc:/resources/images/Athena/common_icons/groupDefault.svg"
                }
            }

            Block {
                title: "ImagePhotoPreview"

                DS3.ImagePhotoPreview {
                    id: imPhPr

                    property var images: [
                        "https://hubs-uploaded-resources.s3.eu-west-1.amazonaws.com/0008D54E_1661785944000_5db07d3b-d337-4ad7-b875-191babb1de84_0000084060c70001_01.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220906T132910Z&X-Amz-SignedHeaders=host&X-Amz-Expires=604799&X-Amz-Credential=AKIAJDTUC7NW72SU5MRQ%2F20220906%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Signature=dcfc9f1bd787d8d389fc6772756d42bc50c55b623f2e2bb984db77b80a15224c",
                        "https://hubs-uploaded-resources.s3.eu-west-1.amazonaws.com/0008D54E_1661785944000_103debbd-ee84-413d-9354-e6f2dea5966f_00000a4060c70001_03.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220906T132910Z&X-Amz-SignedHeaders=host&X-Amz-Expires=604799&X-Amz-Credential=AKIAJDTUC7NW72SU5MRQ%2F20220906%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Signature=c32d5e641ff57f70c6b6cb9595c9f9c6153e2ad0fe0bb62ecb79e713e455f4bf"
                    ]
                    property var imageIndex: 0

                    width: parent.width

                    source: images[imageIndex]

                    onGoNext: imageIndex = imageIndex == 0 ? 1 : 0
                    onGoPrev: imageIndex = imageIndex == 1 ? 0 : 1
                    onDownload: console.log("download")
                }
            }

            Block {
                title: "InfoContainer"

                DS3.InfoContainer {
                    imageType: DS3.InfoContainer.ImageType.PlugImage
                    imageSource: "qrc:/resources/images/Athena/fibra/Help-XL.svg"
                    titleComponent.text: "How to add device"
                    descComponent.text: "The hub is looking for unregistered devices. The process may take a few minutes, please wait."
                }

                DS3.InfoContainer {
                    imageType: DS3.InfoContainer.ImageType.DeviceImage
                    imageSource: Images.get_image("21", "Medium", "WHITE")
                    titleComponent.text: "This is hub device"
                    descComponent.text: "The hub is looking for unregistered devices. The process may take a few minutes, please wait."
                }
            }

            Block {
                title: "InfoContainerImageLoader"

                DS3.InfoContainerImageLoader {
                     titleComponent.text: "Scanning the buses..."
                     descComponent.text: "The hub is looking for unregistered devices. The process may take a few minutes, please wait."
                 }

                DS3.InfoContainerImageLoader {
                     imageComponent.spinner.visible: true
                     titleComponent.text: "Scanning the buses..."
                     descComponent.text: "The hub is looking for unregistered devices. The process may take a few minutes, please wait."
                 }
             }

            Block {
                title: "InputPassword"

                DS3.InputPassword {
                    atomInput.text: "123"
                }

                DS3.InputPassword {
                    atomInput.text: "123"
                    atomInput.label: "Password"
                    isPasswordField: false
                }
            }

            Block {
                title: "InputPhoneNumber | Athena 4.6"

                DS3.Text {
                    text: "phoneNumber = " + inputPhoneNumber.phoneNumber
                }

                DS3.InputPhoneNumber {
                    id: inputPhoneNumber

                    codePicker {
                        currentIndex: 6
                        codeModel: {
                            "+1": "USA",
                            "+12": "ARUBA",
                            "+22": "BELGIUM",
                            "+43": "AUSTRIA",
                            "+46": "SWEDEN",
                            "+333": "FRANCE",
                            "+380": "UKRAINE",
                            "+2345": "IDCOUNTRY"
                        }
                    }
                }
            }

            Block {
                title: "InputPicker"

                DS3.InputPicker {
                    id: cityPicker

                    width: parent.width

                    model: [
                        "Львів", "Київ", "Дніпро", "Житомир", "Запоріжжя", "Івано-Франківськ", "Рівно", "Суми",
                        "Полтава", "Черкаси", "Чернігів", "Кам'янець-Подільський", "Миколі1їв", "Маріуполь", "Харків",
                        "Херсон", "Симферополь", "Слобожанськ", "Сабакін", "Сагакін", "Савакін", "Саракін", "Савокін", "Сарокін"
                    ]
                    notIncludedErrorText: "Оберіть місто зі списку."

                    input {
                        regex: /[А-ЩЬЮЯҐЄІЇа-щьюяґєіїa-zA-Z`'-]{3,50}/ //'
                        atomInput {
                            label: "Місто"
                            placeholderText: "Не обрано"
                        }
                    }
                }
            }

            Block {
                title: "InputPickerDouble"

                DS3.InputPickerDouble {
                    leftPicker {
                        model: [tr.photo_scenario_not_allowed_created_warning_descr, "DoorProtect", "ReX", "FireProtect"]
                        input {
                            atomInput {
                                label: "Що"
                                required: false
                            }
                        }
                    }

                    rightPicker {
                        model: ["Скляренко", "Гуменне", "Львів", "Харків"]
                        input {
                            atomInput {
                                label: "Куди"
                                required: false
                            }
                        }
                    }
                }
            }

            Block {
                title: "InputPickerTriple"

                DS3.InputPickerTriple {
                    leftPicker {
                        model: Array.from(Array(20).keys()).map(el => el * 5)
                        input {
                            atomInput {
                                label: "Скільки"
                            }
                        }
                    }

                    middlePicker {
                        model: ["Hubs", "DoorProtect", "ReX", "FireProtect"]
                        input {
                            atomInput {
                                label: "Чого"
                                required: false
                            }
                        }
                    }

                    rightPicker {
                        model: ["Скляренко", "Гуменне", "Львів", "Харків"]
                        input {
                            atomInput {
                                label: "Куди"
                                required: false
                            }
                        }
                    }
                }

                DS3.InputPickerTriple {
                    leftPicker {
                        model: Array.from(Array(20).keys()).map(el => el * 5)
                        input {
                            atomInput {
                                label: tr.photo_scenario_not_allowed_created_warning_descr
                            }
                        }
                    }

                    middlePicker {
                        model: ["Hubs", "DoorProtect", "ReX", "FireProtect"]
                        input {
                            atomInput {
                                label: "Чого"
                                required: false
                            }
                        }
                    }

                    rightPicker {
                        model: ["Скляренко", "Гуменне", "Львів", "Харків"]
                        input {
                            atomInput {
                                label: "Куди"
                                required: false
                            }
                        }
                    }
                }
            }

            Block {
                title: "InputRemove"

                DS3.InputRemove {
                    atomInput.placeholderText: "Placeholder"
                }

                DS3.Text {
                    text: "In a settingsContainer"
                }

                DS3.SettingsContainer {
                    width: parent.width

                    DS3.InputRemove {
                        atomInput.placeholderText: "Placeholder_1"

                        onRemove: { destroy() }
                    }
                    DS3.InputRemove {
                        atomInput.placeholderText: "Placeholder_2"

                        onRemove: { destroy() }
                    }
                    DS3.InputRemove {
                        atomInput.placeholderText: "Placeholder_3"

                        onRemove: { destroy() }
                    }
                }
             }

            Block {
                title: "InputSingleLine"

                DS3.InputSingleLine {
                    atomInput {
                        label: "Label"
                        placeholderText: "Input text"
                    }
                }

                DS3.InputSingleLine {
                    atomInput {
                        readOnly: true
                        text: "Readonly input"
                        label: "Label"
                        placeholderText: "Input text"
                    }
                }

                DS3.InputSingleLine {
                    atomInput.placeholderText: "Input text"
                }

                DS3.InputSingleLine {
                    atomInput {
                        placeholderText: "Input text"
                        required: true
                    }
                    errorText: "Error text message"
                }
                DS3.InputSingleLine {
                    atomInput {
                        placeholderText: "Input text"
                        required: true
                    }
                    errorText: "Error text message\nMultiple line error message"
                }

                DS3.InputSingleLine {
                    atomInput {
                        label: "Label"
                        placeholderText: "Input text"
                    }
                    rightIcon.source: "qrc:/resources/images/Athena/common_icons/IconHere-M.svg"

                    onRightIconClicked: {
                        console.log("InputSingleLine >2> Clicked")
                    }
                }

                DS3.InputSingleLine {
                    atomInput {
                        label: "Six numbers"
                        validator: RegExpValidator { regExp: /[0-9]{6}/ }
                    }
                    rightIcon {
                        source: "qrc:/resources/images/Athena/common_icons/IconHere-M.svg"
                    }

                    onRightIconClicked: {
                        console.log("InputSingleLine >3> Clicked")
                    }
                }

                DS3.InputSingleLine {
                    atomInput {
                        label: "Six numbers"
                        placeholderText: "Placeholder"
                        required: true
                        validator: RegExpValidator { regExp: /[0-9]{6}/ }
                    }
                }
            }

            Block {
                title: "InputTime"

                DS3.InputTime {
                    time: 65

                    onTimeChanged: () => {
                        console.log(time)
                    }
                }
            }

            Block {
                title: "JsonListModel"

                ListView {
                    width: parent.width
                    height: contentHeight

                    model: DS3.JsonListModel {
                        id: jsonListModel

                        data: [
                            {a: 1, b: 1},
                            {a: 1, b: 2},
                            {a: 2, b: 3},
                        ]
                    }
                    spacing: 2
                    delegate: Rectangle {
                        width: parent.width
                        height: 40

                        color: ui.ds3.bg.low

                        DS3.Text {
                            anchors.centerIn: parent

                            text: b
                        }
                    }
                    section.property: "a"
                    section.criteria: ViewSection.FullString
                    section.delegate: Rectangle {
                        width: parent.width
                        height: 20

                        color: ui.ds3.bg.high

                        DS3.Text {
                            anchors.centerIn: parent

                            text: section
                        }
                    }
                }

                DS3.ButtonContained {
                    text: "Change model"

                    onClicked: jsonListModel.data = [
                        {a: 1, b: 1},
                        {a: (jsonListModel.data[1].a == 1 ? 2 : 1), b: 2},
                        {a: 2, b: 3},
                    ]
                }
            }

            Block {
                title: "MasterCodePicker | Athena 4.6"

                DS3.MasterCodePicker {
                    sheetActionWidth: parent.width
                    codeModel: {
                        "+1": "USA",
                        "+12": "ARUBA",
                        "+22": "BELGIUM",
                        "+43": "AUSTRIA",
                        "+46": "SWEDEN",
                        "+333": "FRANCE",
                        "+380": "UKRAINE",
                        "+2345": "IDCOUNTRY"
                    }
                    currentIndex: 7
                }
            }

            Block {
                title: "MasterCompany"

                DS3.MasterCompany {
                    companyName.text: "First Company"
                }

                DS3.MasterCompany {
                    companyName.text: "Second Company"
                    companyImage.source: "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png"
                }
            }

            Block {
                title: "MasterGroup"

                DS3.MasterGroupM {
                    atomTitle.title: "First Group Title Title Title Title Title Title Title"
                    atomTitle.subtitle: "First Group Subtitle Title Title Title Title Title"
                }

                DS3.MasterGroupM {
                    atomTitle.title: "Second Group Title"
                    atomTitle.subtitle: "Second Group Subtitle"
                    image.source: "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureMedium.png"
                }

                DS3.MasterGroupM {
                    atomTitle.title: "First Group Title Title Title Title Title Title Title"
                    atomTitle.subtitle: "First Group Subtitle Title Title Title Title Title"
                    descText.text: "Description"
                    status: ui.ds3.status.DEFAULT
                }

                DS3.MasterGroupM {
                    atomTitle.title: "First Group Title Title Title Title Title Title Title"
                    atomTitle.subtitle: "First Group Subtitle Title Title Title Title Title"
                    descText.text: "No devices"
                    status: ui.ds3.status.WARNING
                }
            }

            Block {
                title: "MasterUser"

                DS3.MasterUser {
                    atomTitle {
                        title: "Rodion Raskolikov"
                        subtitle: "Rodya@piter.ynul"
                    }
                }

                DS3.MasterUser {
                    atomTitle.title: "Rodion Raskolikov"
                    atomTitle.subtitle: "Rodya@piter.ynul"
                    hasPrivacyOfficerBadge: true
                }
            }

            Block {
                title: "ModalInfo"

                DS3.ButtonContained {
                    onClicked: Popups.popupByPath(
                        "qrc:/resources/qml/components/911/DS3/popups/ModalInfo.qml",
                        {sections: [
                            {
                                "title": "Title",
                                "description": "First message\nSecond message\nThird message"
                            }
                        ]}
                    )
                }
            }

            Block {
                title: "ListView"

                DS3.ListView {
                    width: parent.width
                    height: 200

                    list {
                        model: 3
                        delegate: Rectangle {
                            width: parent.width
                            height: 40

                            color: ui.ds3.bg.high

                            DS3.Text {
                                anchors.centerIn: parent

                                text: modelData
                            }
                        }
                    }
                }
            }

            Block {
                title: "MouseArea"

                Rectangle {
                    width: parent.width
                    height: 300

                    color: area.containsMouse ? ui.ds3.bg.base : ui.ds3.bg.high

                    DS3.MouseArea {
                        id: area
                    }
                }
            }

            Block {
                title: "InputMultiLine"

                DS3.InputMultiLine {
                    atomInputMultiline {
                        label: "Input"
                        text: ""
                    }
                }

                DS3.InputMultiLine {
                    atomInputMultiline {
                        label: "Input"
                        text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Felis donec et odio pellentesque diam volutpat commodo sed. Egestas sed tempus urna et pharetra. Purus non enim praesent elementum facilisis leo. Donec enim diam vulputate ut pharetra sit amet. In nisl nisi scelerisque eu. Ullamcorper eget nulla facilisi etiam. Tristique et egestas quis ipsum suspendisse ultrices. Lectus arcu bibendum at varius vel pharetra vel turpis. Scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique. Risus commodo viverra maecenas accumsan lacus vel. Risus at ultrices mi tempus imperdiet nulla malesuada. Sem viverra aliquet eget sit amet tellus. Iaculis urna id volutpat lacus laoreet non curabitur. Donec et odio pellentesque diam. Sollicitudin ac orci phasellus egestas tellus rutrum tellus pellentesque. Ut enim blandit volutpat maecenas volutpat blandit aliquam etiam. Luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor."
                    }
                }

                DS3.InputMultiLine {
                    atomInputMultiline.text: "Lorem ipsum dolor sit amet."
                }
                DS3.InputMultiLine {
                    atomInputMultiline {
                        text: "Lorem ipsum dolor sit amet."
                        readOnly: true
                    }
                }
            }

            Block {
                title: "NavBarModal"

                DS3.NavBarModal {
                    anchors {
                        top: undefined
                        horizontalCenter: undefined
                    }

                    headerText: "Close"
                    isRound: false
                }

                DS3.NavBarModal {
                    anchors {
                        top: undefined
                        horizontalCenter: undefined
                    }

                    headerText: "Close and Back"
                    showBackArrow: true
                    isRound: false
                }

                DS3.NavBarModal {
                    anchors {
                        top: undefined
                        horizontalCenter: undefined
                    }

                    headerText: "Close and Manual"
                    showManualIcon: true
                    isRound: false
                }

                DS3.NavBarModal {
                    anchors {
                        top: undefined
                        horizontalCenter: undefined
                    }

                    headerText: "Back and Manual"
                    showManualIcon: true
                    showCloseIcon: false
                    showBackArrow: true
                    isRound: false
                }

                DS3.NavBarModal {
                    anchors {
                        top: undefined
                        horizontalCenter: undefined
                    }

                    headerText: "Close, Back and Manual"
                    showManualIcon: true
                    showBackArrow: true
                    isRound: false
                }

                DS3.NavBarModal {
                    anchors {
                        top: undefined
                        horizontalCenter: undefined
                    }

                    headerText: "Is Round"
                }
            }

            Block {
                title: "Pagination"

                Row {
                    spacing: 80

                    DS3.Pagination {
                        amount: 2
                        current: 0
                        firstTriangle: true
                    }

                    DS3.Pagination {
                        amount: 2
                        current: 1
                        firstTriangle: true
                    }
                }

                Row {
                    spacing: 80

                    DS3.Pagination {
                        amount: 2
                        current: 0
                        withBackground: true
                    }

                    DS3.Pagination {
                        amount: 2
                        current: 1
                        withBackground: true
                    }
                }

                Row {
                    spacing: 80
                    DS3.Pagination {
                        amount: 2
                        current: 0
                    }

                    DS3.Pagination {
                        amount: 2
                        current: 1
                    }
                }

                Row {
                    spacing: 64
                    DS3.Pagination {
                        amount: 3
                        current: 0
                    }

                    DS3.Pagination {
                        amount: 3
                        current: 1
                    }

                    DS3.Pagination {
                        amount: 3
                        current: 2
                    }
                }

                Row {
                    spacing: 12
                    DS3.Pagination {
                        amount: 4
                        current: 0
                    }

                    DS3.Pagination {
                        amount: 4
                        current: 1
                    }

                    DS3.Pagination {
                        amount: 4
                        current: 2
                    }

                    DS3.Pagination {
                        amount: 4
                        current: 3
                    }
                }
            }

            Block {
                title: "PlugImage"

                DS3.PlugImage {
                    source: "qrc:/resources/images/Athena/common_icons/Groups-XL.svg"
                }

                DS3.PlugImage {
                    source: "qrc:/resources/images/Athena/common_icons/Groups-XL.svg"
                    smallIcon.source: "qrc:/resources/images/Athena/common_icons/AddSettings-L.svg"
                }

                DS3.PlugImage {
                    source: "qrc:/resources/images/Athena/common_icons/Groups-XL.svg"
                    buttonMini.source: "qrc:/resources/images/Athena/common_icons/Impulse-M.svg"
                }
            }

            Block {
                title: "PlugImageGroup"

                DS3.PlugImageGroup {
                    imageRect.source: "qrc:/resources/images/Athena/groups/Groups-XL-W-BG.svg"
                    enabled: enablingSwitch.checked
                }
            }

            Block {
                title: "PlugImageHero"

                DS3.PlugImageHero {
                    source: "qrc:/resources/images/Athena/migration/HubToFibraImportPartiallySuccess.svg"
                }
            }

            Block {
                title: "PlugImageLoader"

                DS3.PlugImageLoader {}
                DS3.PlugImageLoader {
                    spinner.visible: true
                }
            }

            Block {
                title: "Popup"

                DS3.ButtonContained {
                    onClicked: Popups.popupByPath(
                        "qrc:/resources/qml/components/911/DS3/Popup.qml",
                        {"title": "Popup"}
                    )
                }

                DS3.Popup {
                    id: popupRect

                    destructOnClose: false
                    title: "Long Popup"

                    Rectangle {
                        id: greenrect

                        height: 2000
                        width: 200

                        anchors.horizontalCenter: parent.horizontalCenter

                        color: "#55caa0"
                        radius: 12
                    }
                }

                DS3.ButtonContained {
                    text: "Open long popup"

                    onClicked: popupRect.open()
                }

            }

            Block {
                title: "Popup Dialog"

                DS3.ButtonContained {
                    text: "Dialog with 2 vertical buttons"

                    onClicked: Popups.popupByPath(
                        "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                        {
                            title: tr.error,
                            text: tr.OperationError_AXHubNetworkSettingsOperation_0B_05,
                            firstButtonText: tr.i_will_check,
                            secondButtonText: tr.cancel,
                            isVertical: true
                        }
                    )
                }
            }

            Block {
                title: "Popup Multistep"

                DS3.ButtonContained {
                    text: "Correct multistep"

                    onClicked: Popups.popupByPath(
                        "qrc:/resources/qml/components/911/DS3/popups/PopupMultistep.qml",
                        {"firstStep": "qrc:/resources/qml/components/911/DS3/popups/PopupStepExample.qml"}
                    )
                }

                DS3.ButtonContained {
                    text: "Wrong multistep"

                    onClicked: Popups.popupByPath(
                        "qrc:/resources/qml/components/911/DS3/popups/PopupMultistep.qml",
                        {"firstStep": "qrc:/resources/qml/components/911/DS3/ButtonContained.qml"}
                    )
                }
            }

            Block {
                title: "Popup StatusPopup"

                Timer {
                    id: statusPopupTimer

                    interval: 3000
                    onTriggered: app.actionSuccess()
                }

                Timer {
                    id: statusPopupProgressTimer

                    signal updateProgress

                    repeat: true
                    interval: 1000

                    onTriggered: updateProgress()
                }

                DS3.ButtonContained {
                    text: "StatusPopup Spinner"

                    onClicked: {
                        Popups.please_wait_popup()
                        statusPopupTimer.start()
                    }
                }

                DS3.ButtonContained {
                    text: "StatusPopup ProgressForward"

                    onClicked: {
                        Popups.popupByPath(
                            "qrc:/resources/qml/components/911/DS3/popups/StatusPopup.qml",
                            {
                                "description": tr.request_send,
                                "timeout": 30,
                                "progressUpdateSignals": [statusPopupProgressTimer.updateProgress],
                                "statusType": DS3Popups.StatusPopup.StatusType.ProgressForward,
                            }
                        )
                        statusPopupProgressTimer.start()
                    }
                }
            }

            Block {
                title: "ProgressCountdownM"

                DS3.ProgressCountdownM {
                    id: progressCountdownM

                    time: 5
                }

                DS3.ButtonContained {
                    text: "start"

                    onClicked: progressCountdownM.start()
                }

                DS3.ButtonContained {
                    text: "stop"
                    isAttention: true

                    onClicked: progressCountdownM.stop()
                }

                DS3.ButtonContained {
                    text: "finish"

                    onClicked: progressCountdownM.finish()
                }
            }

            Block {
                title: "ProgressCountdownS"

                DS3.ProgressCountdownS {
                    id: progressCountdownS

                    time: 5
                }

                DS3.ButtonContained {
                    text: "start"

                    onClicked: progressCountdownS.start()
                }

                DS3.ButtonContained {
                    text: "stop"
                    isAttention: true

                    onClicked: progressCountdownS.stop()
                }

                DS3.ButtonContained {
                    text: "finish"

                    onClicked: progressCountdownS.finish()
                }
            }

            Block {
                title: "ProgressBar"

                DS3.ProgressBar {
                    id: progressBar

                    anchors.horizontalCenter: parent.horizontalCenter

                    amount: 100
                    current: 0
                }

                DS3.ButtonContained {
                    width: parent.width

                    anchors.horizontalCenter: parent.horizontalCenter

                    text: {
                        if (progressBarTimer.running) return "Stop progress"
                        if (progressBar.current == 0) return "Start progress"
                        if (progressBar.current == progressBar.amount) return "Restart progress"
                        return "Continue progress"
                    }

                    onClicked: {
                        if (progressBar.current == progressBar.amount) {
                            progressBarTimer.restart()
                            progressBar.current = 0
                            return
                        }
                        if (progressBarTimer.running) return progressBarTimer.stop()
                        return progressBarTimer.start()
                    }
                }

                Timer {
                    id: progressBarTimer

                    interval: 100
                    repeat: true

                    onTriggered: {
                        if (progressBar.current != progressBar.amount) {
                            progressBar.current += 1
                        } else {
                            progressBarTimer.stop()
                        }
                    }
                }
            }

            Block {
                title: "ProgressBarStatus"

                DS3.ProgressBarStatus {
                    id: progressBarStatus

                    amount: 100
                    current: 0
                    statusTexts: [current + "/" + amount, "Other text", "And another one"]
                }

                DS3.ButtonContained {
                    width: parent.width

                    text: {
                        if (progressBarStatusTimer.running) return "Stop progress"
                        if (progressBarStatus.current == 0) return "Start progress"
                        if (progressBarStatus.current == progressBarStatus.amount) return "Restart progress"
                        return "Continue progress"
                    }

                    onClicked: {
                        if (progressBarStatus.current == progressBarStatus.amount) {
                            progressBarStatusTimer.restart()
                            progressBarStatus.current = 0
                            return
                        }
                        if (progressBarStatusTimer.running) return progressBarStatusTimer.stop()
                        return progressBarStatusTimer.start()
                    }
                }

                Timer {
                    id: progressBarStatusTimer

                    interval: 100
                    repeat: true

                    onTriggered: {
                        if (progressBarStatus.current != progressBarStatus.amount) {
                            progressBarStatus.current += 1
                        } else {
                            progressBarStatusTimer.stop()
                        }
                    }
                }
            }

            Block {
                title: "ProgressForward"

                DS3.ProgressForward {
                    id: progressForward
                }

                DS3.ButtonContained {
                    text: "Update progress"

                    onClicked: {
                        progressForward.update()
                    }
                }
            }

            Block {
                title: "NavigationChip"

                DS3.NavigationChip {
                    label: "Navigation Chip"

                    onClicked: selected = !selected
                }
            }

            Block {
                title: "Palette"

                DS3.Text {
                    text: "ui.ds3.figure"
                }

                Component {
                    id: delegateRepeater

                    Row {
                        height: 40
                        width: parent.width

                        spacing: 2

                        Rectangle {
                            height: 40
                            width: 120

                            color: modelData.color
                        }
                        DS3.Text {
                            anchors.verticalCenter: parent.verticalCenter

                            text: modelData.descr_text
                        }
                    }
                }

                Repeater {
                    id: ds3figure

                    model: [
                    {"color": ui.ds3.figure.base, "descr_text": "ui.ds3.figure.base"},
                    {"color": ui.ds3.figure.secondary, "descr_text": "ui.ds3.figure.secondary"},
                    {"color": ui.ds3.figure.nonessential, "descr_text": "ui.ds3.figure.nonessential"},
                    {"color": ui.ds3.figure.disabled, "descr_text": "ui.ds3.figure.disabled"},
                    {"color": ui.ds3.figure.inverted, "descr_text": "ui.ds3.figure.inverted"},
                    {"color": ui.ds3.figure.contrast, "descr_text": "ui.ds3.figure.contrast"},
                    {"color": ui.ds3.figure.interactive, "descr_text": "ui.ds3.figure.interactive"},
                    {"color": ui.ds3.figure.attention, "descr_text": "ui.ds3.figure.attention"},
                    {"color": ui.ds3.figure.positive, "descr_text": "ui.ds3.figure.positive"},
                    {"color": ui.ds3.figure.positiveContrast, "descr_text": "ui.ds3.figure.positiveContrast"},
                    {"color": ui.ds3.figure.warning, "descr_text": "ui.ds3.figure.warning"},
                    {"color": ui.ds3.figure.warningContrast, "descr_text": "ui.ds3.figure.warningContrast"},
                    {"color": ui.ds3.figure.transparent, "descr_text": "ui.ds3.figure.transparent"},
                        ]
                    delegate: delegateRepeater
                }

                DS3.Text {
                    text: "ui.ds3.bg"
                }

                Repeater {
                    id: ds3background

                    model: [
                        {"color": ui.ds3.bg.high, "descr_text": "ui.ds3.bg.high"},
                        {"color": ui.ds3.bg.highest, "descr_text": "ui.ds3.bg.highest"},
                        {"color": ui.ds3.bg.base, "descr_text": "ui.ds3.bg.base"},
                        {"color": ui.ds3.bg.low, "descr_text": "ui.ds3.bg.low"},
                        {"color": ui.ds3.bg.lowest, "descr_text": "ui.ds3.bg.lowest"},
                        {"color": ui.ds3.bg.accent, "descr_text": "ui.ds3.bg.accent"},
                        {"color": ui.ds3.bg.overlay, "descr_text": "ui.ds3.bg.overlay"},
                    ]
                    delegate: delegateRepeater
                }

                DS3.Text {
                    text: "ui.ds3.special"
                }

                Repeater {
                    id: ds3special

                    model: [
                        {"color": ui.ds3.special.knob, "descr_text": "ui.ds3.special.knob"},
                        {"color": ui.ds3.special.hole, "descr_text": "ui.ds3.special.hole"},
                        {"color": ui.ds3.special.divider, "descr_text": "ui.ds3.special.divider"},
                        {"color": ui.ds3.special.white, "descr_text": "ui.ds3.special.white"},
                        {"color": ui.ds3.special.black, "descr_text": "ui.ds3.special.black"},
                        {"color": ui.ds3.special.selection, "descr_text": "ui.ds3.special.selection"},
                    ]
                    delegate: delegateRepeater
                }
            }

            Block {
                title: "ScrollView & ScrollBar"

                Item {
                    width: parent.width
                    height: 300

                    DS3.ScrollView {
                        Rectangle {
                            width: parent.width
                            height: 600

                            color: ui.ds3.bg.base
                        }
                    }
                }

                Item {
                    width: parent.width
                    height: 300

                    DS3.ScrollView {
                        padding: 0

                        Rectangle {
                            width: parent.width
                            height: 600

                            color: ui.ds3.bg.base
                        }
                    }
                }
            }

            Block {
                title: "SelectMulti"

                DS3.SelectMulti {
                    checked: true
                }
            }

            Block {
                title: "SettingsAccordion"

                DS3.SettingsAccordion {
                    width: parent.width
                    title: "Devices"
                    repeaterModel: ["MP", "LC", "FC", "DP"]
                }

                DS3.SettingsAccordion {
                    width: parent.width
                    title: "Devices"
                    repeaterModel: ["MP", "LC", "FC", "DP", "DPP", "MP", "LC", "FC", "DP", "DPP", "MP", "LC", "FC", "DP", "DPP"]
                    hasIcon: true
                    imageSource: "qrc:/resources/images/desktop/icons/bender.gif"
                }
            }


            Block {
                title: "SettingsColorSlider"

                DS3.SettingsColorSlider {
                    title: tr.air_monitor_co_title
                    from: 400
                    to: 2400
                    value: 1000
                    stepSize: 100
                    colorStops: ({
                        0: ui.ds3.figure.positiveContrast,
                        1200: ui.ds3.figure.warningContrast,
                        1600: ui.ds3.figure.attention,
                        2000: ui.ds3.figure.hazard
                    })
                    atomSlider {
                        suffix: ` ${tr.ppm_co_level_value}`
                        minText: "400"
                        maxText: "2,4k"
                    }
                }
            }

            Block {
                title: "SettingsContainer"

                DS3.SettingsContainer {
                    width: parent.width

                    DS3.SettingsSwitch {}
                    DS3.SettingsSwitch {}
                    DS3.SettingsSwitch {}
                }

                DS3.SettingsContainer {
                    width: parent.width

                    title: 'SettingsContainer Title'

                    DS3.SettingsSwitch {}
                    DS3.SettingsSwitch {}
                    DS3.SettingsSwitch {}
                }
            }

            Block {
                title: "SettingsDualSlider"

                DS3.SettingsDualSlider {
                    title: tr.air_monitor_humidity_title
                    from: 0
                    to: 100
                    stepSize: 5
                    firstValue: 30
                    secondValue: 60
                    atomSlider {
                        suffix: "%"
                        minText: "0"
                        maxText: "100"
                    }
                }
            }

            Block {
                title: "SettingsMultiSelection"

                DS3.SettingsMultiSelection {
                    atomTitle.title: "Title"
                }
            }

            Block {
                title: "SettingsNavigationTitlePrimary"

                DS3.SettingsNavigationTitlePrimary {
                    title: "Settings Navigation"
                    subtitle: "Subtitle"
                }

                DS3.SettingsNavigationTitlePrimary {
                    title: "Settings Navigation"
                    subtitle: "Subtitle"
                    companyName: title
                }

                DS3.SettingsNavigationTitlePrimary {
                    title: "Settings Navigation"
                    icon: "qrc:/resources/images/Athena/settings_icons/DeviceTestSettings-L.svg"
                }
            }

            Block {
                title: "SettingsNavigationTitlePrimaryStatus"

                DS3.SettingsNavigationTitlePrimaryStatus {
                    title: "Title"
                    subtitle: "Subtitle"
                    subtitleColor: ui.ds3.figure.secondary
                }

                DS3.SettingsNavigationTitlePrimaryStatus {
                    title: "Title"
                    subtitle: "Subtitle"
                    subtitleColor: ui.ds3.figure.attention
                }

                DS3.SettingsNavigationTitlePrimaryStatus {
                    title: "Title"
                    subtitle: "Subtitle"
                    subtitleColor: ui.ds3.figure.warningContrast
                }

                DS3.SettingsNavigationTitlePrimaryStatus {
                    title: "Title"
                    subtitle: "Subtitle"
                    subtitleColor: ui.ds3.figure.positiveContrast
                }
            }

            Block {
                title: "SettingsTitleSecondaryNavigation"

                DS3.SettingsTitleSecondaryNavigation {
                    title: "Settings Navigation"
                    subtitle: "Subtitle"
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                }

                DS3.SettingsTitleSecondaryNavigation {
                    title: "Settings Navigation"
                    subtitle: "Subtitle"
                    status: ui.ds3.status.WARNING
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                }

                DS3.SettingsTitleSecondaryNavigation {
                    title: "Settings Navigation"
                    subtitle: "Subtitle"
                    status: ui.ds3.status.ATTENTION
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                }

                DS3.SettingsTitleSecondaryNavigation {
                    title: "Settings Navigation"
                    subtitle: "Subtitle"
                    status: ui.ds3.status.HAZARD
                    leftIcon.source: "qrc:/resources/images/Athena/common_icons/SmartphoneRing-M.svg"
                }

                DS3.SettingsTitleSecondaryNavigation {
                    title: "Settings Navigation"
                    subtitle: "Subtitle"
                }
            }

            Block {
                title: "SettingsNavigationSwitchTitlePrimary"

                DS3.SettingsNavigationSwitchTitlePrimary {
                    title: "Settings Navigation"
                    icon: "qrc:/resources/images/Athena/settings_icons/DeviceTestSettings-L.svg"
                }
            }

            Block {
                title: "SettingsPickerTitleSecondary"

                DS3.SettingsPickerTitleSecondary {
                    model: [1, 2, 3, 4, 5, 6, 7]
                    currentIndex: 3
                    atomTitle.title: "SettingsPickerTitleSecondary"
                }

                DS3.SettingsPickerTitleSecondary {
                    model: [1, 2, 3, 4, 5, 6, 7]
                    currentIndex: -1
                    atomTitle.title: "SettingsPickerTitleSecondary"
                }
            }

            Block {
                title: "SettingsSingleSelection"

                DS3.SettingsSingleSelection {
                    atomTitle.title: "Title"
                }
            }

            Block {
                title: "SettingsSliderIcon"

                DS3.SettingsSliderIcon {
                    from: 1
                    to: 20
                    sideIcons: ["qrc:/resources/images/Athena/common_icons/BrightnessLow-M.svg", "qrc:/resources/images/Athena/common_icons/BrightnessHigh-M.svg"]
                }
            }

            Block {
                title: "SettingsSliderValue"

                DS3.SettingsSliderValue {
                    from: 1
                    to: 16
                    value: 4
                    suffix: "A"
                }
            }

            Block {
                title: "SettingsSort"

                DS3.SettingsSort {
                    titleItem.text: "by Name"
                    iconItem {
                        source: "qrc:/resources/images/Athena/common_icons/VerticalArrow-S.svg"
                        color: ui.ds3.figure.interactive
                    }
                }
            }

            Block {
                title: "SettingsSwitch"

                DS3.SettingsSwitch {}

                DS3.SettingsSwitch {
                    title: "The sun was shining on the sea, Shining with all his might: He did his very best to make The billows smooth and bright -- And this was odd, because it was The middle of the night."
                }
            }

            Block {
                title: "SettingsValueSlider"

                DS3.SettingsValueSlider {
                    title: "Settings value slider 1"
                    from: 0
                    to: 50
                    value: 25
                }

                DS3.SettingsValueSlider {
                    title: "Settings value slider 2"
                    from: 0
                    to: 50
                    doubleStepSizeFrom: 16
                    value: 10
                    atomSlider {
                        suffix: "suffix"
                        minText: "MIN"
                        maxText: "MAX"
                    }
                }
            }

            Block {
                title: "SettingsWiFi"

                DS3.SettingsWiFi {
                    title: "Main WiFi"
                    wifiLevel: "NORMAL"
                }

                DS3.SettingsWiFi {
                    title: "Main WiFi"
                    wifiLevel: "NORMAL"
                    isLocked: true
                }
            }

            Block {
                title: "SheetAction"

                DS3.ButtonContained {
                    id: buttonSheetAction

                    onClicked: sheetAction.open()
                }
                DS3.SheetAction {
                    id: sheetAction

                    title: "Title"

                    parent: buttonSheetAction

                    DS3.SettingsSingleSelection {
                        atomTitle.title: "1st"
                        switchChecked: () => console.log("FIRST")
                    }

                    DS3.SettingsSingleSelection {
                        atomTitle {
                            title: "2nd"
                            titleColor: ui.ds3.figure.attention
                        }
                        switchChecked: () => {
                            console.log("SECOND")
                            sheetAction.close()
                        }
                    }
                }
            }

            Block {
                title: "Spacing"

                DS3.Spacing {
                    height: 100
                }
            }

            Block {
                title: "Spinner"

                DS3.Spinner {
                    id: s

                    size: DS3.Spinner.ImageSize.L
                }

                DS3.ButtonContained {
                    onClicked: s.finalize()
                }

                DS3.Spinner {
                    size: DS3.Spinner.ImageSize.M
                }

                DS3.Spinner {
                    size: DS3.Spinner.ImageSize.S
                }
            }

            Block {
                title: "Stepper"

                Row {
                    width: parent.width

                    DS3.Stepper {
                        width: parent.width / 2

                        amount: 2
                        current: 0
                    }

                    DS3.Stepper {
                        width: parent.width / 2

                        amount: 2
                        current: 1
                    }
                }

                Row {
                    width: parent.width

                    DS3.Stepper {
                        width: parent.width / 3

                        amount: 3
                        current: 0
                    }

                    DS3.Stepper {
                        width: parent.width / 3

                        amount: 3
                        current: 1
                    }

                    DS3.Stepper {
                        width: parent.width / 3

                        amount: 3
                        current: 2
                    }
                }
            }

            Block {
                title: "Switch"

                DS3.Switch {
                    checked: true

                    onToggle: () => checked = !checked
                }
            }

            Block {
                title: "TableHeaderXS"

                DS3.TableHeaderXS {
                    titleItem.text: "Table Header XS"

                    buttonIcon.source: "qrc:/resources/images/Athena/common_icons/Settings-M.svg"
                }
            }

            Block {
                title: "TableView"

                DS3.TableView {
                    id: tableScrollView

                    width: parent.width
                    height: 300

                    columnNames: ["H1", "H2", "H3"]
                    fractions: [1,1,1]
                    list {
                        model: 3
                        delegate: Row {
                            height: 160

                            Rectangle {
                                height: parent.height
                                width: tableScrollView.columnWidths[0]

                                color: 'yellow'
                            }
                            Rectangle {
                                height: parent.height
                                width: tableScrollView.columnWidths[1]

                                color: 'pink'
                            }
                            Rectangle {
                                height: parent.height
                                width: tableScrollView.columnWidths[2]

                                color: 'brown'
                            }
                        }
                    }
                }
            }

            Block {
                title: "Tester"

                Item {
                    width: parent.width
                    height: 100

                    DS3.Tester {}
                }
            }

            Block {
                title: "Text"
                DS3.Text {
                    style: ui.ds3.text.title.LBold
                    text: "Title / L-Bold"
                }
                DS3.Text {
                    style: ui.ds3.text.title.MBold
                    text: "Title / M-Bold"
                }
                DS3.Text {
                    style: ui.ds3.text.title.SBold
                    text: "Title / S-Bold"
                }
                DS3.Text {
                    style: ui.ds3.text.title.XSBold
                    text: "Title / XS-Bold"
                }
                DS3.Text {
                    style: ui.ds3.text.title.XSRegular
                    text: "Title / XS-Regular"
                }

                DS3.Spacing { height: 10 }

                DS3.Text {
                    style: ui.ds3.text.body.LBold
                    text: "Body / L-Bold"
                }
                DS3.Text {
                    style: ui.ds3.text.body.LRegular
                    text: "Body / L-Regular"
                }
                DS3.Text {
                    style: ui.ds3.text.body.MBold
                    text: "Body / M-Bold"
                }
                DS3.Text {
                    style: ui.ds3.text.body.MRegular
                    text: "Body / M-Regular"
                }
                DS3.Text {
                    style: ui.ds3.text.body.SBold
                    text: "Body / S-Bold"
                }
                DS3.Text {
                    style: ui.ds3.text.body.XSRegular
                    text: "Body / XS-Regular"
                }

                DS3.Spacing { height: 10 }

                DS3.Text {
                    style: ui.ds3.text.button.MBold
                    text: "Button / M-Bold"
                }
                DS3.Text {
                    style: ui.ds3.text.button.MRegular
                    text: "Button / M-Regular"
                }
                DS3.Text {
                    style: ui.ds3.text.button.SBold
                    text: "Button / S-Bold"
                }

                DS3.Spacing { height: 10 }

                DS3.Text {
                    style: ui.ds3.text.special.BadgeRegular
                    text: "Special / Badge-Regular"
                }
                DS3.Text {
                    style: ui.ds3.text.special.SectionCaps
                    text: "Special / Section-Caps"
                }
            }

            Block {
                title: "TitleCenterAlign"

                DS3.TitleCenterAlign {
                    textItem.text: "TitleCenterAlign"
                }

                DS3.TitleCenterAlign {
                    textItem.text: "imagine that I was able to come up with a long title. i mean a really long one"
                }

                DS3.TitleCenterAlign {
                    textItem.text: "imagine that I was able to come up with a long title. i mean a really long one"
                    isCaps: true
                }
            }

            Block {
                title: "TitleLeftAlign"

                DS3.TitleLeftAlign {
                    textItem.text: "imagine that I was able to come up with a long title. i mean a really long one"
                }

                DS3.TitleLeftAlign {
                    textItem.text: "imagine that I was able to come up with a long title. i mean a really long one"
                    isCaps: true
                }
            }

            Block {
                title: "TitleLeftAlignButton"


                DS3.TitleLeftAlignButton {
                    textItem.text: "TitleLeftAlignButton"
                    buttonText: "Button"
                }

                DS3.TitleLeftAlignButton {
                    textItem.text: "imagine that I was able to come up with a long title. i mean a really long one"
                    isCaps: true
                    buttonText: "Button"
                }
            }

            Block {
                title: "TitleSection"

                DS3.TitleSection {
                    text: "TitleSection"
                }

                DS3.TitleSection {
                    text: "TitleSection"
                    hasButton: true
                    buttonText: "Button"

                    onButtonClicked: () => { console.log("Clicked") }
                }
            }

            Block {
                title: "TitleUniversal"

                DS3.TitleUniversal {
                    text: "TitleUniversal"
                }
            }

            Block {
                title: "UserImage"

                DS3.UserImage {}
                DS3.UserImage {
                    size: 40
                }
            }

            Block {
                title: "UserImageUpload"

                DS3.UserImageUpload {}
            }

            Block {
                title: "UserNavigation"

                DS3.UserNavigation {
                    atomTitle {
                        title: "Rodion Raskolikov"
                        subtitle: "Rodya@piter.ynul"
                    }
                    role: tr.admin
                }

                DS3.UserNavigation {
                    atomTitle {
                        title: "Rodion Raskolikov"
                        subtitle: "Rodya@piter.ynul"
                    }
                    role: tr.pro
                    hasPrivacyOfficerBadge: true
                }
            }

            Block {
                title: "UserRegular"

                DS3.UserRegular {
                    atomTitle {
                        title: "User Name"
                        subtitle: "user@ajax.systems"
                    }
                    role: tr.admin
                    rightIcon.visible: true
                }

                DS3.UserRegular {
                    atomTitle {
                        title: "Alexander Grigorievich Konstantinopolsky Long"
                        subtitle: "User+Multiline+PrivacyOfficer"
                    }
                    role: tr.admin
                    rightIcon.visible: true
                }

                DS3.UserRegular {
                    atomTitle {
                        title: "User Name"
                        subtitle: "user@ajax.systems"
                    }
                    role: tr.admin
                }

                DS3.UserRegular {
                    atomTitle {
                        title: "User Name"
                        subtitle: "user@ajax.systems"
                    }
                    role: tr.user
                    rightIcon.visible: true
                }

                DS3.UserRegular {
                    atomTitle.subtitle: "Liza@irpen.zzz"
                    rightIcon.visible: true
                }

                DS3.UserRegular {
                    atomTitle {
                        title: "User Name"
                        subtitle: "user@ajax.systems"
                    }
                    role: tr.admin
                    hasPrivacyOfficerBadge: true
                    rightIcon.visible: true
                }
            }

            Block {
                title: "UserRemove"

                DS3.UserRemove {
                    atomTitle.subtitle: "user@ajax.systems"
                }
            }

            Block {
                title: "UserSelectionSingle"

                DS3.UserSelectionSingle {
                    atomTitle.title: "User Selection"
                    role: tr.pro
                }
            }

            Block {
                title: "UserSwitch"

                DS3.UserSwitch {
                    enabled: enablingSwitch.checked
                    checked: false
                    atomTitle{
                        title: "Liza@irpen.zzz"
                    }

                    onSwitched: { checked = !checked }
                }

                DS3.UserSwitch {
                    enabled: enablingSwitch.checked
                    checked: false
                    atomTitle{
                        title: "WWWWWWWWWWWWWWWWWWWWWWWW"
                        badge: "ADMIN"
                    }

                    onSwitched: { checked = !checked }
                }
            }
            Block {
                title: "Folder"

                DS3.Folder {
                    labelText: "Devices"
                    selected: true
                }
                DS3.Folder {
                    labelText: "Users"
                    selected: false
                }
                DS3.Folder {
                    labelText: "Hubs"
                    badgeLabel: "1"
                    selected: false
                }
                DS3.Folder {
                    labelText: "Private"
                    badgeLabel: "24"
                    selected: true
                }
            }
            Block {
                title: "FolderControl"

                DS3.FolderControl {
                    onCurrentIndexDiffer: {
                        folderControl.currentIndex = index
                    }

                    enabled: enablingSwitch.checked
                    model:  [
                        { text: "Devices", index: 0 },
                        { text: "Users", index: 1 },
                        { text: "Hubs", index: 3, badgeLabel: "1" },
                        { text: "Private", index: 4, badgeLabel: "24" }
                    ]
                }
            }
            Block {
                title: "GroupNavigation"

                DS3.GroupNavigation {
                    enabled: enablingSwitch.checked
                    groupTitle: "Group Name"
                    groupID: "01"
                    deviceCount: "7"

                    groupRegularClicked: () => {
                        console.log("Main area is clicked")
                    }

                    settingsGearClicked: () => {
                        console.log("Settings gear is clicked")
                    }
                }

                DS3.GroupNavigation {
                    enabled: enablingSwitch.checked
                    groupTitle: "WWWWWWWWWWWWWWWWWWWWWWWW"
                    groupID: "1"
                    deviceCount: "1"

                    groupRegularClicked: () => {
                        console.log("Main area is clicked")
                    }

                    settingsGearClicked: () => {
                        console.log("Settings gear is clicked")
                    }
                }

                DS3.GroupNavigation {
                    enabled: enablingSwitch.checked
                    groupTitle: "No devices"
                    groupID: "2"
                    deviceCount: ""

                    groupRegularClicked: () => {
                        console.log("Main area is clicked")
                    }

                    settingsGearClicked: () => {
                        console.log("Settings gear is clicked")
                    }
                }

                DS3.GroupNavigation {
                    enabled: enablingSwitch.checked
                    groupTitle: "No devices and ID"
                    groupID: ""
                    deviceCount: ""

                    groupRegularClicked: () => {
                        console.log("Main area is clicked")
                    }

                    settingsGearClicked: () => {
                        console.log("Settings gear is clicked")
                    }
                }
            }
            Block {
                title: "PlugImage"

                DS3.PlugImage {
                    source: "qrc:/resources/images/Athena/common_icons/Groups-XL.svg"
                }
            }
            Block {
                title: "PlugImageCircle"

                DS3.PlugImageCircle {
                    icon: "qrc:/resources/images/Athena/common_icons/COIllustration.svg"
                    iconColor: ui.ds3.figure.base
                }
            }
            Block {
                title: "PlugImageGroup"

                DS3.PlugImageGroup {
                    imageRect.source: "qrc:/resources/images/Athena/common_icons/Groups-XL.svg"
                }
            }

            Block {
                title: "ContextLoader"

                DS3.ButtonContained {
                    width: parent.width

                    text: "Update context"

                    onClicked: app.changeNewArchitectureExample()
                }

                Root.ContextLoader {
                    width: parent.width
                    height: childrenRect.height

                    contextTarget: app.newArchitectureExample
                }
            }

            Block {
                title: "ButtonRect"

                DS3.ButtonContainedRect {
                    text: "ButtonContainedRect"

                    status: DS3.ButtonRect.Status.Default
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Asterisk-S.svg"
                    enabled: false

                    onClicked: {
                        console.log("ButtonContainedRect")
                    }
                }

                DS3.ButtonContainedRect {
                    text: "ButtonContainedRect"

                    status: DS3.ButtonRect.Status.Attention
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Asterisk-S.svg"

                    onClicked: {
                        console.log("ButtonContainedRect")
                    }
                }

                DS3.ButtonTextRect {
                    text: "ButtonTextRect"

                    status: DS3.ButtonRect.Status.Secondary
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Asterisk-S.svg"

                    onClicked: {
                        console.log("ButtonTextRect")
                    }
                }

                DS3.ButtonTextRect {
                    text: "ButtonTextRect"

                    status: DS3.ButtonRect.Status.Secondary
                    buttonIconSource: "qrc:/resources/images/Athena/common_icons/Asterisk-S.svg"
                    enabled: false

                    onClicked: {
                        console.log("ButtonTextRect")
                    }
                }

                DS3.ButtonTextRect {
                    text: "ButtonTextRect"

                    status: DS3.ButtonRect.Status.Default
                    badge.text: "42"

                    onClicked: {
                        console.log("ButtonTextRect")
                    }
                }
            }

            Block {
                title: "ButtonSelect"

                DS3.ButtonSelect {
                    text: "Button"
                }
            }

            Block {
                title: "Select"

                DS3.Select {
                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }

                DS3.Select {
                    isRound: true

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }

                DS3.Select {
                    hasBackground: true
                    checked: true
                    enabled: false

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }

                DS3.Select {
                    hasBackground: true
                    checked: true

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }
            }

            Block {
                title: "Reset All"

                DS3.ResetAll {
                    size: DS3.ResetAll.ComponentSize.L

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }

                DS3.ResetAll {
                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }

                DS3.ResetAll {
                    size: DS3.ResetAll.ComponentSize.S

                    enabled: false
                    checked: true

                    clickedArea.onClicked: {
                        checked = !checked
                    }
                }
            }

            Block {
                title: "MRtable"

                DS3.TableView {
                    id: hubList

                    width: parent.width
                    height: parent.height

//                    anchors.top: tmp.top  // it does not works anyway yet. Comment it to hide log-error

                    columnNames: [tr.number, tr.a911_object, tr.a911_hub_id]
                    fractions: [1,1,1]
                    list {
                        model: 3
                        delegate: Row {
                            height: 56

                            Rectangle {
                                height: parent.height
                                width: hubList.columnWidths[0]

                                color: 'yellow'
                            }
                            Rectangle {
                                height: parent.height
                                width: hubList.columnWidths[1]

                                color: 'pink'
                            }
                            Rectangle {
                                height: parent.height
                                width: hubList.columnWidths[2]

                                color: 'brown'
                            }
                        }
                    }
                }
            }
        }
    }
}
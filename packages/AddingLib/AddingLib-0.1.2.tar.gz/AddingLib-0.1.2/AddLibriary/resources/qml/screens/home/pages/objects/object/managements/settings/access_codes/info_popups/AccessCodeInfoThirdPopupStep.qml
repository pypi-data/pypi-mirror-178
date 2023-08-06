import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.PopupStep {
    DS3.InfoContainer {
        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/access_codes/KeyPadAction-XL.svg"
        titleComponent.text: tr.access_codes_wizard_third_step_title
        descComponent.text: tr.access_codes_wizard_third_step_descr
    }
    DS3.Spacing { height: 24 }
}
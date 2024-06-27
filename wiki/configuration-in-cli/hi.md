# CLI इंटरफ़ेस में विन्यास आयात कर रहे हैं<
## Saving configuration

**This feature is available from version: `3.3`**

If you prefer command-line interface (CLI) before graphical user interface (GUI), SaveDesktop in addition to saving configuration in the GUI, allows you save configuration in the CLI.

### So how to proceed?

**1. Open a terminal**

You can open it from the applications menu, or by using the Ctrl+Alt+T keyboard shortcut.

**2. Type the command to import the configuration**

Enter the following command in the terminal:
- if you have SaveDesktop installed as a Flatpak package, use the following:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --save-now
     ```

- if you have SaveDesktop installed as a Snap or native package, use:
     ```
     savedesktop --save-now
     ```

When using this method, it uses parameters from the GUI, specifically parameters from the periodic saving mode, such as filename format and selected folder for periodic saving files. You can save the configuration with this method whenever you want, regardless of the selected periodic saving interval.

## Importing configuration

**यह सुविधा इस संस्करण से उपलब्ध है: `3.2.2`**

GUI में विन्यास आयात करने के अलावा, SaveDesktop आपको कमांड लाइन इंटरफ़ेस (CLI) में विन्यास आयात करने की भी अनुमति देता है, जिसका उपयोग आप अपने डेस्कटॉप वातावरण के टूटने की स्थिति में कर सकते हैं।

### तो कैसे आगे बढ़ें?
**1. एक टर्मिनल खोलें**

आप इसे एप्लिकेशन मेनू से या Ctrl+Alt+T कीबोर्ड शॉर्टकट का उपयोग करके खोल सकते हैं।

**2. विन्यास आयात करने के लिए कमांड टाइप करें**

टर्मिनल में निम्नलिखित कमांड दर्ज करें:
- यदि आपने SaveDesktop को Flatpak पैकेज के रूप में स्थापित किया है, तो निम्नलिखित का उपयोग करें:

     ```
     flatpak run io.github.vikdevelop.SaveDesktop --import-config /path/to/filename.sd.tar.gz
     ```

- यदि आपने SaveDesktop को Snap या नेटिव पैकेज के रूप में स्थापित किया है, तो इसका उपयोग करें: 
     ```
     savedesktop --import-config /path/to/filename.sd.tar.gz
     ```

**टिप्पणी**:
- `/path/to/filename.sd.tar.gz` के बजाय, उस विन्यास संग्रह का पथ दर्ज करें जिसे आप आयात करना चाहते हैं, उदाहरण के लिए: `/home/user/Downloads/myconfig.sd.tar.gz`

_यदि आपके कोई प्रश्न हैं, तो आप GitHub मुद्दों का उपयोग कर सकते हैं।_

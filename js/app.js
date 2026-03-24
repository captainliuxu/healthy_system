function appendMessage(role, text) {
    const chatArea = document.getElementById("chatArea");
    if (!chatArea) return;

    const msg = document.createElement("div");
    msg.classList.add("msg", role);
    msg.textContent = text;

    chatArea.appendChild(msg);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function getFakeReply(userText) {
    const text = userText.trim();

    if (text.includes("头晕")) {
        return "你提到了头晕，建议今晚测量一次血压，并先注意休息。";
    }

    if (text.includes("忘") && text.includes("药")) {
        return "如果你今天忘记服药，建议先确认本次用药时间，不要自行重复加量。";
    }

    if (text.includes("血压")) {
        return "如果你刚测了血压，可以把结果记录下来，我可以继续帮你分析趋势。";
    }

    if (text.includes("难受") || text.includes("不舒服")) {
        return "听起来你现在状态不太好，建议先休息一下，并留意今天的症状变化。";
    }

    if (text.includes("睡") || text.includes("失眠")) {
        return "睡眠也会影响慢病管理，今晚尽量早点休息，避免情绪和指标波动。";
    }

    return "我已经记下了你的情况。你也可以继续告诉我今天是否按时服药、有没有测量血压。";
}

function sendMessage() {
    const input = document.getElementById("chatInput");
    if (!input) return;

    const text = input.value.trim();
    if (!text) return;

    appendMessage("user", text);
    input.value = "";

    setTimeout(() => {
        const reply = getFakeReply(text);
        appendMessage("ai", reply);
    }, 500);
}

function triggerProactiveMessage() {
    const messages = [
        "现在是晚间服药时间，记得按计划完成用药。",
        "你今天还没有记录血压，建议今晚尽快测量一次。",
        "你最近提到过头晕，今晚注意休息，并留意身体状态。",
        "慢病管理最重要的是长期规律，坚持记录会更有帮助。"
    ];

    const randomIndex = Math.floor(Math.random() * messages.length);
    appendMessage("ai", messages[randomIndex]);
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("chatInput");
    if (!input) return;

    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
let selectedMedication = "";
let selectedSymptom = "";

function selectOption(button) {
    const group = button.dataset.group;
    const value = button.dataset.value;

    const buttons = document.querySelectorAll(`.choice-btn[data-group="${group}"]`);
    buttons.forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");

    if (group === "medication") {
        selectedMedication = value;
    }

    if (group === "symptom") {
        selectedSymptom = value;
    }
}

function saveRecord() {
    const systolic = document.getElementById("systolic")?.value || "";
    const diastolic = document.getElementById("diastolic")?.value || "";
    const note = document.getElementById("note")?.value || "";
    const saveResult = document.getElementById("saveResult");

    const recordData = {
        medication: selectedMedication,
        systolic: systolic,
        diastolic: diastolic,
        symptom: selectedSymptom,
        note: note,
        time: new Date().toLocaleString()
    };

    localStorage.setItem("healthRecord", JSON.stringify(recordData));

    if (saveResult) {
        saveResult.style.display = "block";
        saveResult.textContent = "今日记录已保存";
    }
}
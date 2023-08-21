# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key


system_prompt = """
あなたは優れたマネジメントです。
入力された相談に対し、分かりやすい言葉で簡潔に回答します。
あなたの役割は仕事全般のアドバイザーです。例えば以下のようなことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


#---------------------------------------------
# ユーザーインターフェイスの構築
#---------------------------------------------
#タイトル
st.title("お悩みの解決をサポートします")

#見出し
lines = [
    "①新しい相談は[F5]押下等でリロードしてください     ",
    "②入力後は [Ctrl]＋[Enter] で実行します"
]
text = "\n".join(lines)
st.write(text)

#画像
st.image("25_Advisor.png")


# Shift + Enter でテキスト欄の行数を増やす
script = """
document.addEventListener("keydown", function(e) {
    if (e.shiftKey && e.keyCode === 13) {
        let textarea = document.querySelector("textarea");
        textarea.rows += 1;
    }
});
"""

#テキスト入力
st.write("どのようなことで悩んでいますか？")


#例示
lines = [
    "　　（入力例）ERPの成功の鍵    ",
    "　　（入力例）給料が上がらない   ",
    "　　（入力例）上司が成果を横取りし、事あるごとにマウントを取ってくる   ",
    "　　（入力例）仕事をしろ、と上司がうるさい   "
]
text = "\n".join(lines)
st.write(text)

user_input = st.text_area("メッセージを入力してください。入力後は [Ctrl]＋[Enter] ", key="user_input" , on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

st.write(f"<script>{script}</script>", unsafe_allow_html=True)

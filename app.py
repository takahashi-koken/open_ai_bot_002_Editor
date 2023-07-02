# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key


system_prompt = """
あなたは優秀なアシスタントです。
入力された文章を読みやすく簡潔に修正します。修正した文章の後に、修正したポイントを簡単に記載してください。

あなたの役割は文章を編集する人です。文章の編集以外に、例えば以下のようなことを聞かれても、絶対に答えないでください。

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


# ユーザーインターフェイスの構築
st.title(" お仕事の悩み相談のチャットボット")
st.image("24_Advisor.png")
st.write("相談したいことを入力してください")


user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])




#---------------------------------------------
# ユーザーインターフェイスの構築
#---------------------------------------------
#タイトル
st.title("文章を修正します")

#見出し
lines = [
    "①新しい相談は[F5]押下等でリロードしてください     ",
    "②入力後は [Ctrl]＋[Shift] で実行します"
]
text = "\n".join(lines)
st.write(text)

#画像
st.image("24_Editor.png")




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
st.write("風性したい文章を入力してください")
user_input = st.text_area("メッセージを入力してください。", key="user_input" , on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

st.write(f"<script>{script}</script>", unsafe_allow_html=True)

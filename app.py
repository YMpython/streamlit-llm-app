import streamlit as st
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
import os

# 環境変数の読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="AI専門家相談アプリ",
    page_icon="🤖",
    layout="wide"
)

def get_llm_response(user_input, expert_type):
    """
    LLMからの回答を取得する関数
    
    Args:
        user_input (str): ユーザーの入力テキスト
        expert_type (str): 専門家の種類
        
    Returns:
        str: LLMからの回答
    """
    
    # 専門家のタイプに応じたシステムメッセージを設定
    expert_prompts = {
        "プログラミング専門家": "あなたはプログラミングとソフトウェア開発の専門家です。技術的な質問に対して、具体的なコード例や最適な解決策を提案してください。",
        "健康・医療専門家": "あなたは健康と医療の専門家です。健康に関する質問に対して、科学的根拠に基づいた情報を提供してください。ただし、診断や治療の代替ではないことを明記してください。",
        "ビジネス・経営専門家": "あなたはビジネスと経営の専門家です。経営戦略、マーケティング、起業に関する質問に対して、実践的なアドバイスを提供してください。",
        "教育・学習専門家": "あなたは教育と学習の専門家です。学習方法、教育理論、スキルアップに関する質問に対して、効果的な学習戦略を提案してください。"
    }
    
    system_message = expert_prompts[expert_type]
    
    try:
        # ChatOpenAIモデルを初期化
        chat_model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # メッセージを作成
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_input)
        ]
        
        # LLMに送信して回答を取得
        response = chat_model(messages)
        
        return response.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def main():
    # タイトル
    st.title("🤖 AI専門家相談アプリ")
    
    # アプリの説明
    st.markdown("""
    ## 📋 アプリの概要
    このアプリは、様々な分野の専門家AIに相談できるサービスです。
    質問したい分野を選択し、質問内容を入力することで、その分野の専門家として回答します。
    
    ## 🚀 使用方法
    1. **専門家を選択**: ラジオボタンから相談したい分野の専門家を選択してください
    2. **質問を入力**: テキストエリアに質問や相談内容を入力してください
    3. **送信**: 「相談する」ボタンをクリックして回答を受け取ってください
    
    ---
    """)
    
    # 専門家の選択
    expert_type = st.radio(
        "相談したい専門家を選択してください:",
        [
            "プログラミング専門家",
            "健康・医療専門家", 
            "ビジネス・経営専門家",
            "教育・学習専門家"
        ]
    )
    
    # 選択された専門家の説明
    expert_descriptions = {
        "プログラミング専門家": "💻 プログラミング、ソフトウェア開発、技術的な問題解決について相談できます",
        "健康・医療専門家": "🏥 健康管理、医療知識、予防医学について相談できます（診断・治療の代替ではありません）",
        "ビジネス・経営専門家": "💼 経営戦略、マーケティング、起業、ビジネス全般について相談できます",
        "教育・学習専門家": "📚 学習方法、教育理論、スキルアップについて相談できます"
    }
    
    st.info(expert_descriptions[expert_type])
    
    # 質問入力
    user_input = st.text_area(
        "質問や相談内容を入力してください:",
        height=100,
        placeholder="例: Pythonでファイルを読み込む方法を教えてください"
    )
    
    # 送信ボタン
    if st.button("🚀 相談する", type="primary"):
        if user_input.strip():
            with st.spinner("専門家が回答を準備中です..."):
                # LLMから回答を取得
                response = get_llm_response(user_input, expert_type)
                
                # 回答を表示
                st.success("✅ 回答が完了しました！")
                st.markdown("### 📝 専門家からの回答:")
                st.write(response)
                
        else:
            st.warning("⚠️ 質問内容を入力してから「相談する」ボタンを押してください。")
    
    # サイドバーに使用上の注意
    with st.sidebar:
        st.markdown("## ⚠️ 使用上の注意")
        st.markdown("""
        - **健康・医療相談**: 提供される情報は一般的な知識であり、医師の診断や治療に代わるものではありません
        - **プログラミング相談**: 提供されるコードは参考例です。実際の使用前に十分テストしてください
        - **ビジネス相談**: 市場状況や個別の事情により結果は異なる場合があります
        - **教育相談**: 個人差があるため、自分に合った方法を見つけることが重要です
        """)

if __name__ == "__main__":
    main()
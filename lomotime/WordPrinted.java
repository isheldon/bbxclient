import java.awt.Color;
import java.awt.Font;

public class WordPrinted {

	private String word = "";

	private Font font;
	
	private String fontName = "方正静蕾简体";
	
	private int fontStyle =  Font.BOLD;
	
	private int wordNumPerLine = 8;
	
	private int totalNum = wordNumPerLine * 2;
	
	private Color fontColor = Color.BLACK;
	
	public static final double PER = 0.90;

	public WordPrinted() {
	}
	
	public WordPrinted(String fontName, int fontStyle) {
		this.fontName = fontName;
		this.fontStyle = fontStyle;
	}

	public void setWordNumPerLine(int wordNumPerLine) {
		this.wordNumPerLine = wordNumPerLine;
		this.totalNum = wordNumPerLine * 2;
	}
	
	public String getWord() {
		return word;
	}

	public void setWord(String word) {
		this.word = word;
	}

	public Font getFont() {
		return font;
	}

	public String getFontName() {
		return fontName;
	}

	public int getFontStyle() {
		return fontStyle;
	}

	public void setFont(Font font) {
		this.font = font;
	}

	public int getWordNumPerLine() {
		return wordNumPerLine;
	}

	public int getTotalNum() {
		return totalNum;
	}

	public Color getFontColor() {
		return fontColor;
	}

	public void setFontColor(Color fontColor) {
		this.fontColor = fontColor;
	}
}

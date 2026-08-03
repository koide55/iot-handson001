// 簡易的な認証用の秘密鍵（センサー側と一致させる）
const API_KEY = 'YOUR_API_KEY';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    if (data.apiKey !== API_KEY) {
      return ContentService.createTextOutput(JSON.stringify({ ok: false, error: 'unauthorized' }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('data');
    if (!sheet) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('data');
      sheet.appendRow(['timestamp', 'temperature', 'humidity', 'pressure', 'userid']);
    }

    sheet.appendRow([
      new Date(),
      data.temperature,
      data.humidity,
      data.pressure,
      data.userid || ''
    ]);

    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

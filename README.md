# oss-tracker

Gerçek, sürdürülebilir açık kaynak katkısı için kişisel takip sistemi.

Bu repo, GitHub contribution grafiğini **sahte commit'lerle şişirmek** için değil,
gerçek PR/issue katkılarını bulmayı, planlamayı ve kaydetmeyi kolaylaştırmak için var.

## Nasıl çalışır

1. `.github/workflows/daily-issue-scan.yml` her gün otomatik çalışır ve
   `scripts/find_issues.py` script'ini tetikler.
2. Script, GitHub Search API üzerinden şu dillerde açık
   `good first issue` / `help wanted` etiketli issue'ları tarar:
   - Python
   - JavaScript / TypeScript
   - Dart (Flutter)
3. Sonuçlar [`ISSUES.md`](./ISSUES.md) dosyasına yazılır. İçerik değişmediyse
   commit atılmaz (boş/sahte commit yok).
4. Bir issue'ya PR açtığında [`CONTRIBUTIONS.md`](./CONTRIBUTIONS.md) dosyasına
   şu komutla kaydını eklersin:

   ```bash
   ./scripts/log_contribution.sh <repo> <pr_url> <dil> "<kısa açıklama>"
   ```

## Neden sahte commit script'i yok

GitHub'ın Acceptable Use Policies'i contribution grafiğini yapay olarak şişirmeyi
"inauthentic activity" sayar ve bu tespit edilirse hesap kısıtlanabilir/rozetler
geri alınabilir. Bu repo bunun yerine **gerçek katkı hacmini artırmayı** hedefler:
doğru issue'yu bulmak çoğu zaman en büyük engeldir, bu yüzden o kısmı otomatikleştirdik.

## Kurulum

```bash
gh secret set GH_SEARCH_TOKEN --body "$(gh auth token)"  # opsiyonel, rate limit için
```

Varsayılan olarak workflow `secrets.GITHUB_TOKEN` kullanır, bu genellikle yeterlidir.

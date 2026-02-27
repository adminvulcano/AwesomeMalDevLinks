# https://blog.levi.wiki/post/2025-12-06-decondition-enumerator

# Decondition Enumerator

This is a continuation of the earlier [Decondition Everything](https://blog.levi.wiki/post/2025-12-05-decondition-everything) post.

## Cooldown Time

I.e. when the cache is reset after `a_pi == Detected` (known bad) or `a_pi == cutoff` (deconditioned).

From testing: can be as little as **5-15 minutes**

## How does the Process Identification work?

### Test-Conduction

- Define a single difference between `A.exe` and `A'.exe`
- execute `A.exe` to be detected, i.e. no deconditioning
- then execute `A'.exe` with deconditioning

  - if also detected => `PI(A.exe) == PI(A'.exe)` --\> expected
  - if not detected => `PI(A.exe) != PI(A'.exe)` --\> unexpected, may give a hint how PI works
- example:

```
.\LsassReader\tested\LsassReader-compile1.exe
> no decon
> detected

.\LsassReader\tested\LsassReader-compile2.exe 20
> 20 rounds of decon
> still detected --> same PI --> expected
```

### Test-Files

Tested exe files see [Decondition-Enumerator/LsassReader/tested/](https://github.com/cailllev/Decondition-Enumerator/tree/master/LsassReader/tested).

### Test-Results

- Exe Name different: PI same
- Compile Date different: PI same
- Imphash (+SSDeep +TLSH) different: PI same
- ???
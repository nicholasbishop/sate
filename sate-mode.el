(setq sate-highlights
      '(("\\[.+\\]" . font-lock-function-name-face)))

(defvar sate-mode-syntax-table nil "Syntax table for `sate-mode'.")

(setq sate-mode-syntax-table
      (let ((syntable (make-syntax-table)))

        ;; comments start with '#' and go to end of line
        (modify-syntax-entry ?# "<" syntable)
        (modify-syntax-entry ?\n ">" syntable)

        (modify-syntax-entry ?\[ "(" syntable)
        (modify-syntax-entry ?\] ")" syntable)

        (modify-syntax-entry ?\( "(" syntable)
        (modify-syntax-entry ?\) ")" syntable)

        ;; return it
        syntable))

(define-derived-mode sate-mode fundamental-mode "sate"
  "Major mode for satefiles."
  (setq-local comment-start "#")
  (setq-local comment-use-syntax t)
  (setq-local font-lock-defaults '(sate-highlights))
  (set-syntax-table sate-mode-syntax-table))

(add-to-list 'auto-mode-alist '("\\.satefile\\'" . sate-mode))

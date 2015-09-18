

; Make sure all our packages are installed
(defvar sontek-packages
  '(clojure-mode gist magit markdown-mode sass-mode scss-mode yaml-mode
        projectile yasnippet undo-tree csv-mode rainbow-mode nose
        pytest git-commit rainbow-delimiters move-text jedi deferred
        flycheck flymake flymake-python-pyflakes flymake-easy flymake-cursor
        multiple-cursors ack-and-a-half dash s etags-select smartscan
   )
  "A list of packages to ensure are installed at launch.")

(dolist (p sontek-packages)
  (when (not (package-installed-p p))
    (package-install p)))

(require 'multiple-cursors)
(require 'ack-and-a-half)
(require 'projectile)

(smartscan-mode 1)

(projectile-global-mode)

(setq projectile-tags-command "ctags -e -R --extra=+fq --exclude=.git --exclude=.tox --exclude=.tests -f ")

(defun my-find-tag ()
  (interactive)
  (if (file-exists-p (concat (projectile-project-root) "TAGS"))
      (visit-project-tags)
    (build-ctags))
  (etags-select-find-tag-at-point))

(defun visit-project-tags ()
  (interactive)
  (let ((tags-file (concat (projectile-project-root) "TAGS")))
    (visit-tags-table tags-file)
    (message (concat "Loaded " tags-file))))

(global-set-key (kbd "M-.") 'my-find-tag)


;; On the fly syntax checking
(require 'flycheck)
(global-flycheck-mode)
(setq flycheck-highlighting-mode 'lines)

(add-hook 'python-mode-hook #'(lambda () (setq flycheck-checker 'python-pylint)))

(require 'flymake-python-pyflakes)
(eval-after-load 'flymake '(require 'flymake-cursor))

(add-hook 'python-mode-hook 'flymake-python-pyflakes-load)
(setq flymake-python-pyflakes-executable "flake8")

; Handle non-unqiue buffers better
(setq uniquify-buffer-name-style 'forward)
(require 'undo-tree)
(global-undo-tree-mode 1)

(require 'rainbow-delimiters)
(global-rainbow-delimiters-mode)

(require 'move-text)
(move-text-default-bindings)

; Configure whitespace settings to display when we are over 80chars
(setq whitespace-style '(face empty tabs lines-tail trailing))
(setq whitespace-line-column 79)
(global-whitespace-mode 1)
(setq-default fill-column 79)

;(load-theme 'solarized-dark t)

;; no startup msg
(setq inhibit-startup-message t)

; turn on paren match highlighting
(show-paren-mode 1)

; highlight entire bracket expression
(setq show-paren-style 'expression)

; display line numbers in margin
(global-linum-mode 1)

; display the column and line our cursor is on
(column-number-mode 1)

; stop creating those backup~ files
(setq make-backup-files nil)

; stop creating those #autosave# files
(setq auto-save-default nil)

; highlight the current line we are editing
(global-hl-line-mode 1)

; disable the toolbar
(tool-bar-mode -1)

; disable the menubar
(menu-bar-mode -1)

; Never insert tabs
(setq-default indent-tabs-mode nil)

; Allow creating lines above and below
(defun open-line-below ()
  (interactive)
  (end-of-line)
  (newline)
  (indent-for-tab-command))

(defun open-line-above ()
  (interactive)
  (beginning-of-line)
  (newline)
  (forward-line -1)
  (indent-for-tab-command))

(global-set-key (kbd "<C-return>") 'open-line-below)
(global-set-key (kbd "<C-M-return>") 'open-line-above)

(defun add-py-debug ()
      "add debug code and move line down"
    (interactive)
    (move-beginning-of-line 1)
    (insert "import pdb; pdb.set_trace();\n"))

(defun annotate-pdb ()
  (interactive)
  (highlight-lines-matching-regexp "import pdb")
  (highlight-lines-matching-regexp "pdb.set_trace()"))

(add-hook 'python-mode-hook 'annotate-pdb)

(defun python-add-breakpoint ()
  (interactive)
  (newline-and-indent)
  (insert "import ipdb; ipdb.set_trace()")
  (highlight-lines-matching-regexp "^[ ]*import ipdb; ipdb.set_trace()"))

(add-hook 'python-mode-hook
    (lambda ()
        (define-key python-mode-map (kbd "C-c C-p") 'python-add-breakpoint)))

(setq c-default-style "linux"
      c-basic-offset 4)

(defun show-onelevel ()
  "show entry and children in outline mode"
  (interactive)
  (show-entry)
  (show-children))

(defun cjm-outline-bindings ()
  "sets shortcut bindings for outline minor mode"
  (interactive)
  (local-set-key [?\C-,] 'hide-sublevels)
  (local-set-key [?\C-.] 'show-all)
  (local-set-key [C-up] 'outline-previous-visible-heading)
  (local-set-key [C-down] 'outline-next-visible-heading)
  (local-set-key [C-left] 'hide-subtree)
  (local-set-key [C-right] 'show-onelevel)
  (local-set-key [M-up] 'outline-backward-same-level)
  (local-set-key [M-down] 'outline-forward-same-level)
  (local-set-key [M-left] 'hide-subtree)
  (local-set-key [M-right] 'show-subtree))

(add-hook 'outline-minor-mode-hook
          'cjm-outline-bindings)

(add-hook 'python-mode-hook
          '(lambda ()
             (outline-minor-mode)
             (setq outline-regexp " *\\(def \\|clas\\|#hea\\)")
             (hide-sublevels 1)))
   

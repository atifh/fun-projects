;; ----------------------
;; Final newline handling
;; ----------------------
(setq require-final-newline t)

(setq next-line-extends-end-of-buffer nil)
(setq next-line-add-newlines nil)

(load "~/.emacs.d/package.el")
(load "~/.emacs.d/init.el")

;; ---------
;; TAB Setup
;; ---------
(setq-default tab-width 4
	      standard-indent 4
	      indent-tabs-mode nil
              tab-width 8)
;;; Key Mappings
(global-set-key "\C-ca" 'auto-fill-mode)
(global-set-key "\C-cw" 'woman)         ;WOMAN
(global-set-key "\C-q" 'hippie-expand)
(global-set-key "\C-ccl" 'whitespace-cleanup)
(global-set-key "\C-c\C-k" 'copy-line)
(global-set-key [f11] 'fullscreen)
(global-set-key [f5] 'revert-all-buffers)
;; (global-set-key [f6] 'magit-status)
(global-set-key [(meta p)] 'insert-debug-clause)
(global-set-key [(meta P)] 'delete-debug-clause)
;; (global-set-key [f7] 'insert-appengine_debug-clause)
(global-set-key "\C-c\o" 'load-file)
;; (global-set-key [f7] 'psvn)

;; (set-default-font "Bitstream Vera Sans Mono-10")
(set-default-font "DejaVu Sans Mono-16")
;;; Color Theme
(load "~/.emacs.d/atif/color-theme-g0sub.el")
(require 'color-theme-g0sub)
(color-theme-g0sub)

;; -----------------
;; Insert time stamp
;; -----------------
(defun insert-date ()
  "Insert current date and time."
  (interactive "*")
  (insert (current-time-string)))

;; ----------------------------------------
;; Kill current buffer without confirmation
;; ----------------------------------------
(global-set-key "\C-xk" 'kill-current-buffer)
(defun kill-current-buffer ()
  "Kill the current buffer, without confirmation."
  (interactive)
  (kill-buffer (current-buffer)))

;; ESK specific
(defun turn-on-highlight-parens-mode ()
  (highlight-parentheses-mode 1))
 
(add-hook 'coding-hook 'turn-on-highlight-parens-mode)
(remove-hook 'coding-hook 'turn-on-hl-line-mode)
(remove-hook 'clojure-mode-hook 'idle-highlight)
(remove-hook 'emacs-lisp-mode-hook 'idle-highlight)
 
;; ------------
;; General Info
;; ------------
(setq user-mail-address "mail@atifhaider.com")
(setq user-full-name "Atif Haider")

;; ---------
;; Templates
;; ---------
(load "~/.emacs.d/atif/template.el")
(require 'template)
(template-initialize)

;;; --------
;;; SVN
;;; -------
;; (require 'psvn)l
;; ------
;; Python
;; ------
(setq python-mode-hook
      '(lambda () (progn
                    (set-variable 'py-indent-offset 4)
                    (set-variable 'py-smart-indentation nil)
                    (set-variable 'indent-tabs-mode nil))))

(eval-after-load "python-mode"
  '(progn
    (add-hook 'python-mode-hook 'auto-fill-mode)))

;; Uniquify
(require 'uniquify)
(eval-after-load 'uniquify
  '(progn
     (setq uniquify-buffer-name-style 'reverse)
     (setq uniquify-separator "/")
     (setq uniquify-after-kill-buffer-p t) ; rename after killing uniquified
     (setq uniquify-ignore-buffers-re "^\\*")))

;; Useful utility functions
(defun revert-all-buffers()
  "Refreshs all open buffers from their respective files"
  (interactive)
  (let* ((list (buffer-list))
         (buffer (car list)))
    (while buffer
      (if (string-match "\\*" (buffer-name buffer)) 
          (progn
            (setq list (cdr list))
            (setq buffer (car list)))
          (progn
            (set-buffer buffer)
            (revert-buffer t t t)
            (setq list (cdr list))
            (setq buffer (car list))))))
  (message "Refreshing open files"))

(defun rename-file-and-buffer (new-name)
  "Renames both current buffer and file it's visiting to NEW-NAME."
  (interactive "sNew name: ")
  (let ((name (buffer-name))
	(filename (buffer-file-name)))
    (if (not filename)
	(message "Buffer '%s' is not visiting a file!" name)
        (if (get-buffer new-name)
            (message "A buffer named '%s' already exists!" new-name)
            (progn (rename-file name new-name 1)
                   (rename-buffer new-name)
                   (set-visited-file-name new-name)
                   (set-buffer-modified-p nil))))))

(defun move-buffer-file (dir)
  "Moves both current buffer and file it's visiting to DIR."
  (interactive "DNew directory: ")
  (let* ((name (buffer-name))
	 (filename (buffer-file-name))
	 (dir
          (if (string-match dir "\\(?:/\\|\\\\)$")
              (substring dir 0 -1) dir))
	 (newname (concat dir "/" name)))
    (if (not filename)
	(message "Buffer '%s' is not visiting a file!" name)
        (progn (copy-file filename newname 1)
               (delete-file filename)
               (set-visited-file-name newname)
               (set-buffer-modified-p nil)
               t))))

;; -----
;; Tramp
;; -----

(eval-after-load "tramp"
  '(progn
    (setq tramp-default-method "ssh")))


(defun fullscreen ()
  (interactive)
  (set-frame-parameter nil 'fullscreen
                       (if (frame-parameter nil 'fullscreen) nil 'fullboth)))

;; Let Emacs point out some ugliness in my Python code
(defface invalid-face
  '((t (:background "Red" :underline t)))
  "Face used to highlight invalid constructs or other ugliness"
  )

(defun python-strict-mode ()
  (font-lock-add-keywords 'python-mode
                          '(("^\\s *\t" . 'invalid-face)
                            ("[ \t]+$" . 'invalid-face)
                            ("^[ \t]+$" . 'invalid-face))
                          ))

(add-hook 'python-mode-hook 'python-strict-mode)

;;; Clojure
;; (clojure-slime-config "/home/atif/src")


;; insert flagged debug statement
(defun insert-debug-clause () (interactive)
  "Insert a fresh debugging printf()-statement and position point in it"
  (insert-string "import pdb;pdb.set_trace();\n")
  (python-indent-line)
  ;; (previous-line 2)
  ;; (forward-word 3)
  ;; (forward-char 3)
  )

;; insert flagged debug statement for appengine
(defun insert-appengine_debug-clause () (interactive)
  "Insert a fresh debugging printf()-statement and position point in it"
  (insert-string "from debug import set_trace;set_trace();\n")
  (python-indent-line))

;; remove flagged debug statements
(defun delete-debug-clause () (interactive)
  "eliminate sections bounded by /* DEBUG / <stuff> / DEBUG */"
  (save-excursion
    (goto-char (point-min))
    (replace-regexp 
     "import ipdb;ipdb.set_trace();\n"
     "")))

;;; Twitter
;; (load "~/.emacs.d/atif/twittering-mode.el")
;;  (require 'twittering-mode)
;;  (setq twittering-username "")
;;  (setq twittering-password "") ; This is optional

(defun start-twittering-quick* ()
  (interactive)
  (delete-other-windows)
  ;; (full-screen-toggle)
  (twittering-mode)

  (split-window-horizontally)
  (other-window 1)
  (twittering-search "#clojure")

  (split-window-horizontally)
  (other-window 1)
  (twittering-search "#python")

  (split-window-horizontally)
  (other-window 1)
  (twittering-replies-timeline)
  
  (balance-windows)
  (rotate-windows)
  (rotate-windows)
  (rotate-windows))


;; CoffeeScript mode
(add-to-list 'load-path "~/.emacs.d/vendor/coffee-mode")
(require 'coffee-mode)
(add-to-list 'auto-mode-alist '("\\.coffee$" . coffee-mode))
(add-to-list 'auto-mode-alist '("Cakefile" . coffee-mode))
(setq-default tab-width 4)

;; Indentation configuration.
(defun coffee-custom ()
  "coffee-mode-hook"
 (set (make-local-variable 'tab-width) 2))

(add-hook 'coffee-mode-hook
  '(lambda() (coffee-custom)))


;; ;; Scala mode
;; (add-to-list 'load-path "~/.emacs.d/scala-mode2/")
;; (require 'scala-mode2)

;; (add-to-list 'load-path "~/.emacs.d/ensime/elisp/")
;; (require 'ensime)
;; (add-hook 'scala-mode-hook 'ensime-scala-mode-hook)

;; (push "/opt/scala/bin/" exec-path)
;; (push "/opt/sbt/" exec-path)

;; (add-hook 'scala-mode-hook
;;           '(lambda ()
;;              (yas/minor-mode-on)))

;; (setq yas/my-directory "~/.emacs.d/scala-mode/contrib/yasnippet/snippets")
;; (yas/load-directory yas/my-directory)

;; clojure-mode
;; (add-to-list 'load-path "~/opt/clojure-mode")
;; (require 'clojure-mode)

;; paredit
;; (add-to-list 'load-path "~/opt/paredit")
;; (require 'paredit)

;; slime
;; (eval-after-load "slime" 
;;   '(progn (slime-setup '(slime-repl))	
;; 	(defun paredit-mode-enable () (paredit-mode 1))	
;; 	(add-hook 'slime-mode-hook 'paredit-mode-enable)	
;; 	(add-hook 'slime-repl-mode-hook 'paredit-mode-enable)
;; 	(setq slime-protocol-version 'ignore)))

;; (add-to-list 'load-path "~/opt/slime")
;; (require 'slime)
;; (slime-setup)
;; (setq byte-compile-warnings '(not nresolved
;;                                   free-vars
;;                                   callargs
;;                                   redefine
;;                                   obsolete
;;                                   noruntime
;;                                   cl-functions
;;                                   interactive-only
;;                                   ))
;; (add-hook 'w3-parse-hooks 'w3-tidy-page)
;; (defvar w3-fast-parse-tidy-program "c:\\tidy")
;;   (defun w3-tidy-page (&optional buff)
;;     "Use html tidy to clean up the HTML in the current buffer."
;;     (save-excursion
;;         (if buff
;; 	    (set-buffer buff)
;;           (setq buff (current-buffer)))
;;         (widen)
;;         (call-process-region (point-min) (point-max)
;; 	   	             w3-fast-parse-tidy-program
;; 			     t (list buff nil) nil ;nil nil nil;
;; 			     "--show-warnings" "no" "--show-errors" "0" "--force-output" "yes"
;; 			     "-quiet" "-clean" "-bare" "-omit"
;; 			     "--drop-proprietary-attributes" "yes" "--hide-comments" "yes"
;; 			   )))

# Makefile for source rpm: gnome-session
# $Id$
NAME := gnome-session
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
